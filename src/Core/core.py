"""
    Furnivall core functions
"""
import uuid, os, logging, common
import Assignment, Workunit
import Personality
import Plugins, Views

from tornado import web
from tornado.options import define, options
from tornado.escape import json_decode

class UserManager(object):

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
        username=self.db.get("select user from auth where user='%s'\
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

class ObjectManager(web.RequestHandler, UserManager):
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

        job=Jobs.job(researcher.initialized_views[viewfile],
                getattr(getattr(Plugins, view.plugin), view.class_)())
        if researcher: researcher.jobs.append(job)

    def assign_view_to_researcher(self, viewfile, researcher):
        """
            This has to be called before adding a job to a researcher, in order
            to initialize the view. This will start the view's main class and
            add the created objects to initialized_views object.
        """
        if researcher:
            enabled_vf=self.application.conf('enabled_views', viewfile)
            viewObject_=getattr(getattr(Views, viewfile), enabled_vf)
            researcher.initialized_views[viewfile]=ViewOjbect_(self.application)

    def user_can_perform(self, user_perms, perms, check_for_all):
        """
            Check if a user can perform certain actions.
        """
        if check_for_all:
            return [ i for i in user_perms if i not in perms ] == []
        else:
            return [ i for i in user_perms if i in perms ] != []

    # TODO: Add the auth module to tornado, from : https://github.com/bkjones/Tinman/commit/152301d68c86ac7524cf4391b1f98f68c59b2408#diff-1
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
            user_id=self.get_secure_cookie('user')
            user=self.application.users[user_id]
            viewfile=self.get_argument('viewfile')

            if "job" in slug and self.user_can_perform(permissions,
                    ['own_job'], False):
                self.assign_job_to_researcher(viewfile, researcher)

            if "view" in slug and self.user_can_perform(permissions,
                    ['assign_view'], 'view', False):
                self.assign_view_to_researcher(viewfile, researcher)

        except:
            viewfile=False
            researcher=False

        self.redirect(self.get_argument('next', '/'))

class Scheduler(ObjectManager):

    def assign_task(self, view):
        """
            Get a free task, if user_ is doing that task, return an error
        """
        free_task=self.getfreetask()
        if get_current_user()[0] is free_task.user_.id_:
            logging.debug('[Debug] Not creating user, not return task... User\
                    is already doing that task, something failed!')
            return
        logging.debug('[Debug] Creating user_ object. Giving it to a task')

        self.getfreetask(view).user_ = get_current_user()

    def getworkunit(self, job):
        """
            Return a workunit object, a new one if no unnasigned workunits
            available
        """
        for wk in job.workunits:
            logging.debug('Trying to return a free workunit.\
                    Currently processing %s' %(wk))
            if not wk.status:
                logging.debug('%s is free!' %wk)
                return wk

        # No free workunits.
        logging.debug("No free workunits.\
                Creating new workunit object from %s", job)

        # FIXME:
        # This is what makes job.produce_workunits to need returning one...
        # And it doesn't look nice. It isn't any problem, just not nice
        return job.produce_workunits()


    def getfreetask(self, view):
        """
            If user is able to execute a determinated view task,
            get a workunit and return the task
            with better scommon, and with no session_id.
            If user is able to execute the task, but no pre-created
            (and not assigned) tasks are available, return a new task.
            Should iterate trough a researcher pool, getting jobs, then
            split jobs in view, job, and check view's compatibility.

        """
        # TODO: change ScommonMatch in workunit to call the plugin/view's compatibility class. TODO: Make a view's compatibility class
        for researcher in self.application.researchers:
            logging.debug('Processing researcher %s' %researcher)
            for job in researcher.jobs:
                logging.debug('Processing job %s' %job)
                for view, job in job:
                    logging.debug('Processing view and job %s %s' %(view, job))
                    if job.viewObject.check_view(self.get_current_user()):
                        logging.debug("View is supported by user (ViewOjbect: %s) (user_: %s)" %(job.viewObject, self.get_current_user()))
                        wk=self.getworkunit(job)
                        task=[sort(task, key=lambda t: t.ScommonMatch()) for task in wk.tasks if not task.user_.session_id ][0] # Get the best task ordered by ScommonMatch if it has not a user_ assigned
                        if task: return task
                        else: return wk.new_task()
        return

    @property
    def user_tasks(self, user=False, status=False):
        """
            Return tasks in status "ok" and "failed" from a user_

        """
        if not user:
            user, auth=self.get_current_user()

        if not status:
            tasks_finished=self.application.tasks_true[:]
            tasks_finished.expand(self.application.tasks_false)
            return [task for task in user.tasks if task in tasks_finished ]
        else:
            return user.tasks

class Application(common.CommonFunctions, tornado.web.Application):
    def __init__(self):
        """
            Sets up the tornado web server
        """

        self.read_config()
        urls=[
                ("/([^/]+)", self.MainHandler),
                ("/", self.MainHandler),
                ("/new/([^/]+)", ObjectManager),
                ]

        settings=dict(
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                xsrf_cookies=True,
                cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        )

        special_login_slugs={
                'root': '/Admin/',
                'researcher': '/Admin/Researcher',
                'user': '/User/Home'
        }

        logging.info('Loading Furnival main application')
        logging.debug('Researchers initialized from database: %s' %self.researchers)
        logging.debug('Starting server with urls: %s' %urls)
        self.researchers=self.InitializeResearchers() # Here we do the part on restoring from database.
        tornado.web.Application.__init__(self, urls, **settings)

    def InitializeResearchers(self):
        """
            Initialize researchers, foreach researcher stored in database, recreate it
            Actually, it's returning an empty set, as persistence is not implemented.
        """
        # Initially, this can be like this, as we've not implemented persistence yet'.
        self.created_jobs={} # Don't delete, when views are created, they need a created_jobs argument in the creator. # TODO Make this use the queues
        self.views=deque() # Make this use the queues
        self.jobs={}
        self.workunits={}
        self.tasks={}
        return {}

    class MainHandler(Scheduler):
        """
            MainHandler, inherits tornado's requesthandler and shows up display templastes
        """

        def login(self):
            """
                Checks out login against a database, given username and passwor as url params
                and sets out a cookie.
            """

            username = self.get_argument("username", "")
            password = self.get_argument("password", "")
            auth = db.get("select permissions from auth where user='%s' and pass='%s'"
                    %(username, password))
            db_user = db.get("select id as id_ from auth where user='%s' and pass='%s'"
                    %(username, password))
            try: return ( db_user.id_, auth.permissions )
            except: return

        def get_higher_permission(self, permissions):
            if "root" in permissions: return "root"
            if "researcher" in permissions: return "researcher"
            else: return "user"

        def get(self, slug=False):
            """
                Tornado RequestHandler get function, renders slug as called
                from tornado, passing jobs and slug as argument.
                It also checks arguments to take actions when arguments are provided
            """
            # Dirty hack, seems like passing a default to get_argument is not working
            try:
                self.get_argument('next')
            except:
                self.request.arguments['next']="/"

            auth="None" # Default user permissions is None

            if not slug: # Default to landing if /view/ called. TODO: Do this as / too
                logging.debug('[DEBUG] Defining slug as default')
                slug="Landing"

            if "Login" in slug:
                user_id, auth=self.login()
                self.set_secure_cookie('username', user_id)
                user, auth=self.get_current_user() # Get user after login (from cookie set in login process)
                logging.debug('Logging in for user: %s' %user)
                slug=self.application.special_login_slugs[self.get_higher_permission(auth)]

            if slug is "Logout":
                self.clear_cookie('username')
                self.clear_cookie('permissions')
                slug="Login"

            logging.debug('[Debug] Rendering template %s' %slug)
            logging.debug('User has %s permissions' %auth)

            self.render('%s' %(slug),
                    user_permissions=auth,
                    views=self.application.views,
                    jobs=self.application.created_jobs,
                    researchers=self.application.researchers,
                    slug=slug )

            try:
                if self.get_argument('get_task'):
                    self.assign_task(self.get_argument('view'))
            except:
                pass
