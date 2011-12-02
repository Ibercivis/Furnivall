"""
    Furnivall user management
"""
import logging
import Core.Assignment, Core.WorkUnit, Core.Personality
import Plugins

from tornado import web
from tornado.options import define, options
from tornado.escape import json_decode

class UserManager(web.RequestHandler):

    """
        Credential management.
    """

    def get_current_user(self):
        """
            Gets current user from cookie AND permissions (so this will do
            when user logged in)
        """
        return (self.get_secure_cookie('user', self.get_secure_cookie('perms')))

    def validate_user(self, user, password):
        username = self.db.get("select user from auth where user='%s'\
            and password ='%s'" %(
                self.get_argument('user'),
                self.get_argument('pass', '')
                )
            ).user
        self.set_secure_cookie('user', username)
        if not username: return False

        if self.get_argument('user') == "anonymous":
            self.set_secure_cookie('perms', 'view_task')
            return True

        auth = self.db.get("select permissions from auth where user='%s' "
            %(username)).permissions
        self.set_secure_cookie('perms', auth )
        return True

class ObjectManager(UserManager):
    """
        Object manager, creation, delete and modify petitions should go here.
        Right now, it's able to assign a session to a user, a job and a view to
        a researhcer.
    """

    def assign_job_to_researcher(self, viewfile, researcher):
        """
            Having a the view filename (wich is used in views pool),
            create a jobs object with the view object from the views pool.
        """

        job = Jobs.Job(researcher.initialized_views[viewfile],
                getattr(getattr(Plugins, view.plugin), view.class_)(),
                self.application)
        if researcher: researcher.jobs.append(job)

    def assign_view_to_researcher(self, viewfile, researcher):
        """
            This has to be called before adding a job to a researcher, in order
            to initialize the view. This will start the view's main class and
            add the created objects to initialized_views object.
            TODO: This has to be wrong... it's impossible for it to work
            But it was working three months ago.
        """
        if researcher:
            enabled_vf = self.application.conf('enabled_views', viewfile)
            view_object_ = getattr(getattr(Views, viewfile), enabled_vf)
            researcher.initialized_views[viewfile] = ViewOjbect_(self.application)

    def user_can_perform(self, user_perms, perms, check_for_all):
        """
            Check if a user can perform certain actions.
        """
        if check_for_all:
            return [ i for i in user_perms if i not in perms ] == []
        else:
            return [ i for i in user_perms if i in perms ] != []

    # TODO: Add the auth module to tornado, from :
    # https://github.com/bkjones/Tinman/commit/152301d68c86ac7524cf4391b1f98f68c59b2408#diff-1
    @require_basic_auth('Furnivall', self.validate_user)
    def get(self, slug=False):
        """
            Object manager get function.
            Creates as requested jobs or views
            TODO: Document user permissions for the ACL:
                own_job
                create_job
                view_job
                own_task
                create_task
                view_task
                own_workunit
                create_workunit
                view_workunit
                root

                If we want a task to create another task, the assigned user_ has to have own_task permissions!
                Note: For a task to create another task, I'd prefer it to be done via the web interface.
                We can do it at plugin level, but that would mean we wouldn't have such a nice access to authentication methods.
        """

        user_id, permissions = self.get_current_user()
        logging.debug("Creating new -%s-" %slug)

        try:
            user_id = self.get_secure_cookie('user')
            user = self.application.users[user_id]
            viewfile = self.get_argument('viewfile')

            if "job" in slug and self.user_can_perform(permissions,
                    ['own_job'], False):
                self.assign_job_to_researcher(viewfile, researcher)

            if "view" in slug and self.user_can_perform(permissions,
                    ['assign_view'], 'view', False):
                self.assign_view_to_researcher(viewfile, researcher)

        except:
            viewfile = False
            researcher = False

        self.redirect(self.get_argument('next', '/'))
