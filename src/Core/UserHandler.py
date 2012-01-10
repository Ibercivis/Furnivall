"""
    Furnivall user management
"""
import logging
import Core.Assignment
import Plugins

from tornado import web


class ObjectManager(web.RequestHandler):
    """
        Object manager, creation, delete and modify petitions should go here.
        Right now, it's able to assign a session to a user, a job and a view to
        a researhcer.
    """

    def validate_user(self, user, password):
        username = self.application.db.get("select user from auth\
            where user='%s' and password ='%s'"
            %( self.get_argument('user'), self.get_argument('pass', ''))).user

        self.set_secure_cookie('user', username)
        if not username: return False

        if self.get_argument('user') == "anonymous":
            self.set_secure_cookie('perms', 'view_task')
            return True

        auth = self.application.db.get("select permissions from\
                auth where user='%s' " %(username)).permissions
        self.set_secure_cookie('perms', auth )
        return True

    def assign_job_to_user(self, viewfile, researcher):
        """
            Having a the view filename (wich is used in views pool),
            create a jobs object with the view object from the views pool.
        """

        job = Jobs.Job(user.initialized_views[viewfile],
                getattr(getattr(Plugins, view.plugin), view.class_)(),
                self.application)
        user.jobs.append(job)

    def assign_view_to_user(self, viewfile, user):
        """
            This has to be called before adding a job to a researcher, in order
            to initialize the view. This will start the view's main class and
            add the created objects to initialized_views object.
        """
        enabled_vf = self.application.conf('enabled_views', viewfile)
        user.initialized_views[viewfile] = getattr(getattr(Views, viewfile),
            enabled_vf)(self.application)

    def check_perms(self, user_perms, perms, check_for_all):
        """
            Check if a user can perform certain actions.
        """
        if check_for_all:
            return [ i for i in user_perms if i not in perms ] == []
        else:
            return [ i for i in user_perms if i in perms ] != []

    # TODO: Add the auth module to tornado, from :
    # https://github.com/bkjones/Tinman/commit/152301d68c86ac7524cf4391b1f98f68c59b2408#diff-1
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


        import logging
        try:

            user_id = self.get_secure_cookie('username')
            viewfile = self.get_argument('viewfile')
            user = self.application.db['users'][user_id]
            perms = user.permissions

            logging.debug("Creating new -%s-" %slug)

            if "job" == slug and self.check_perms(perms, ['own_job'], False):
                self.assign_job_to_user(viewfile, user)

            if "view" == slug and self.check_perms(perms,
                    ['assign_view'], False):
                logging.debug("Assigning %s to %s", viewfile, user)
                self.assign_view_to_user(viewfile, user)

        except Exception, error:
            logging.debug(error)
            viewfile = False
            user = False

        self.redirect(self.get_argument('next', '/'))
