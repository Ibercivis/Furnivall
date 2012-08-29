"""
    Furnivall user management
"""

import logging, uuid
from Furnivall.Core import Assignment, Jobs
from Furnivall import Plugins, Views
from tornado import web

class UserManager(web.RequestHandler):
    """
        Handle login, and when asked for return current user object from database.
    """
    def get_current_user(self):
        """
            Gets user set in "username" cookie from database.
            If not present, tries to log-in.
        """
        request_username = self.get_argument('username', False)
        cookie_username = self.get_secure_cookie('username')
        if not cookie_username and request_username:
            return self.login() # If there is no cookie set but there's
        elif cookie_username:
            try:
                return self.application.db['users'][cookie_username]
            except:
                return False

    def login(self):
        """
            Checks out login against a database, given username and password
            as args and sets out a cookie.
        """
        try:
            username = self.get_argument("username", False)
            password = self.get_argument("password", False)
            assert username and password # Umm... nice.
            if self.application.db['users'][username].password == password:
                self.set_secure_cookie('username', username)
                return self.application.db['users'][username]
        except KeyError:
            logging.info("Bad auth for %s", username)
        except AssertionError:
            logging.info("Someone tried to login with empty username or password")

        return False

class ObjectManager(UserManager):
    """
        Object manager, creation, delete and modify petitions should go here.
        Right now, it's able to assign a session to a user, a job and a view to
        a researhcer.
    """

    def get_views_list(self):
        """
            Returns a list of all views (wich are initialized
            on server restart) available in Views module.
        """
        return Views.ViewClasses.keys()

    def assign_job_to_user(self, viewfile, user):
        """
            Having a the view filename (wich is used in views pool),
            create a jobs object with the view object from the views pool.
        """
        view = self.application.db['users'][user].initialized_views[viewfile]
        plugin = getattr(getattr(Plugins, view.plugin), view.class_)()
        parent_uuid = uuid.uuid4().__str__()
        try:
            self.application.db['users'][user].jobs[parent_uuid] = ""
        except Exception, error:
            logging.error("Error resetting uuid in db")
        self.application.db['users'][user].jobs[parent_uuid] =\
            Jobs.Job(view, plugin, self, parent_uuid, user)
        self.application.db['users'][user].jobs[parent_uuid].produce_initial_workunits()

    def assign_view_to_user(self, viewfile, user):
        """
            This has to be called before adding a job to a researcher, in order
            to initialize the view. This will start the view's main class and
            add the created objects to initialized_views object.
        """
        user = self.application.db['users'][user]
        for viewclass in Views.ViewClasses[viewfile]:
            user.initialized_views[viewfile] = getattr(getattr(Views,
                 viewfile), viewclass)(self.application)

    def assign_task_to_user(self, viewfile, user):
        """
            Creates a task assigned to the logged-in researcher.
            You can modify it later from the plug-in with
            assign
        """
        work = self.get_argument("workunit")
        job = self.get_argument("job")
        number = self.get_argument('number')
        try:
            job = self.application.db['users'][user].jobs[job]
            job.workunits[work].create_tasks(number, self.application.db['users'][user])
        except Exception, error:  
            logging.debug("Could not create tasks %s", error)

    def check_perms(self, user_perms, perms, check_for_all):
        """
            Check if a user can perform certain actions.
        """
        if "root" in perms:
            logging.info("Of course")
            return True

        if check_for_all:
            return [ i for i in user_perms if i not in perms ] == []
        else:
            return [ i for i in user_perms if i in perms ] != []


    # TODO: Add the auth module to tornado, from :
    # https://github.com/bkjones/Tinman/commit/152301d68c86ac7524cf4391b1f98f68c59b2408#diff-1
    def do_management(self, slug):
        """
            Object manager get function.
            Creates as requested jobs or views
            Implement this user permissions on the ACL:

            * own_job
            * create_job
            * view_job
            * own_task
            * create_task
            * view_task
            * own_workunit
            * create_workunit
            * view_workunit
            * root

            If we want a task to create another task, the assigned user_ has to have own_task permissions!
            Note: For a task to create another task, I'd prefer it to be done via the web interface.
            We can do it at plugin level, but that would mean we wouldn't have such a nice access to authentication methods!
        """

        action = "assign" if "view" == slug else "own"
        user_id = self.get_secure_cookie('username')
        viewfile = self.get_argument('viewfile', False)
        if user_id == "root" and self.get_argument('researcher', False):
            user = self.application.db['users'][self.get_argument('researcher')]
            perms = [ 'root' ]
        else:
            user = self.application.db['users'][user_id]
            perms = user.permissions

        if not self.check_perms(action + "_" + slug, perms, False):
            self.write("Not allowed")

        try:
            a = getattr(self, "assign_%s_to_user" %(slug))(viewfile, user_id)
        except Exception, error:
            logging.info(error)
            self.write("Could not create %s: %s" %(slug, error))

        self.redirect('/home')

    def get(self, slug=False):
        return self.do_management(slug)

    def post(self, slug=False):
        return self.do_management(slug)
