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
        return (self.get_secure_cookie('user', self.get_secure_cookie('perms')

    def login(self):
        """
            Login and set up secure cookie credentials
            Note: Right now, I'm using http basic auth, so this might not be used.
            But it's ok if it's used anyway
        """
        try:
            if not self.get_secure_cookie('user'):
                return (None, None)
            else:
                return ( self.get_secure_cookie('user'),
                    self.get_secure_cookie('perms') )

        except Exception,e:
            logging.debug('User not allowed because of:%s' %e)
            return ("None", "None")

    def validate_user(self, user, password):
        username=self.db.get("select user from auth where user='%s'\
            and password ='%s'" %(
                self.get_argument('user'),
                self.get_argument('pass', '')
                )
            ).user
        self.set_secure_cookie('user', username)
        if not username: return (None, None)
        auth = self.db.get("select permissions from auth where user='%s' "
            %(username)).permissions
         self.set_secure_cookie('perms', auth )

        return (username, auth)

class ObjectManager(web.RequestHandler, UserManager):
    """
        Object manager, creation, delete and modify petitions should go here.
        Right now, it's able to assign a session to a user, a job and a view to
        a researhcer. 
    """

    def assign_session_to_user(self, volunteer):
        """
            Creates a unique session id and assigns it to volunteer object.
            then, it returns the volunteer with host and user data.
        """
        auuid=uuid.uuid4()
        self.session.user_id=auuid # Assign user id to session.
        logging.debug("Creating user %s,%s,%s",
                auuid, self.session.host, self.session.user)
        return volunteer.set_data(self.session.host, self.session.user, auuid )

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

    # We make it authed, should use self.get_current_user ... 
    # TODO: Check it, some people reports problems.
    @require_basic_auth('Furnivall', self.validate_user)
    def get(self, slug=False):
        """
            Object manager get function.
            Creates as requested jobs or views
            TODO: make it create tasks too, in case it's needed, and according 
            to job create tasks permissions.
        """
        
        user_id, permissions = self.get_current_user()
        logging.debug("Creating new -%s-" %slug)

        try:
            if researcher in permissions:
                user_id=self.get_secure_cookie('user')
                researcher=self.application.researchers[user_id]

            viewfile=self.get_argument('viewfile')

            if "researcher" in permissions or :

            if "job" in slug:
                self.assign_job_to_researcher(viewfile, researcher)
            if "view" in slug:
                self.assign_view_to_researcher(viewfile, researcher) 
        except:
            viewfile=False
            researcher=False

        self.redirect(self.get_argument('next', '/'))

class Scheduler(ObjectManager):

    def assign_task(self, view):
        """
            Get a free task, if volunteer is doing that task, return an error
        """
        free_task=self.getfreetask()
        if get_current_volunteer() is free_task.volunteer: 
            logging.debug('[Debug] Not creating user, not return task... User\
                    is already doing that task, something failed!')
            return
        logging.debug('[Debug] Creating volunteer object. Giving it to a task')
        assign_session_to_user(self.getfreetask(view).volunteer)

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

    def get_current_volunteer(self):
        """
            Get current volunteer, by session id (session_id is
            scheduler-specific, should be for each user)
            If no session_id, calls assign_session_to_user
        """

        session_id=self.get_secure_cookie('session_id')

        if not session_id:
            return assign_session_to_user
        else:
            logging.debug('Getting volunteer object for id: %s' %(session_id))
            return self.application.volunteers[session_id]

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
                    if job.viewObject.check_view(self.get_current_volunteer()):
                        logging.debug("View is supported by user (ViewOjbect: %s) (Volunteer: %s)" %(job.viewObject, self.get_current_volunteer()))
                        wk=self.getworkunit(job)
                        task=[sort(task, key=lambda t: t.ScommonMatch()) for task in wk.tasks if not task.volunteer.session_id ][0] # Get the best task ordered by ScommonMatch if it has not a volunteer assigned
                        if task: return task
                        else: return wk.new_task()
        return 

    def get_done_tasks(self):
        """
            Return tasks in status "ok" and "failed" from a volunteer's tasks_fail and tasks_ok pools.
        """
        atasks=[]
        volunteer=self.get_current_volunteer()
        logging.debug('Getting done tasks for volunteer: %s' %volunteer)
        for workunit in self.find_volunteer_workunits(volunteer):
            atasks.extend([task in self.find_volunteer_tasks(volunteer, workunit.tasks_ok, workunit.tasks_fail)])
        logging.debug('got %s' %atasks)
        return atasks

    def find_volunteer_workunits(self, user):
        """
            Generator returning volunteer workunits. Warning: this might be dangerous, as we've seen that
            generators seem to not work Ok when removing elements from its object.
        """

        logging.debug('Getting workunits for volunteer: %s' %volunteer)
        for workunit in user.workunits:
            yield workunit 

    def find_volunteer_tasks(self, volunteer, tasks_ok, tasks_fail):
        """
            return tasks from tasks_ok and task_fail if they're from volunteer
        """
        logging.debug('Getting all tasks for volunteer %s', volunteer)
        tasks_ok.extend(tasks_fail)
        return [ task for task in tasks_ok if task.volunteer is volunteer ]

class Application(common.CommonFunctions, tornado.web.Application):
    def __init__(self):
        """
            Creates a list of researchers, wich SHOULD (todo) contain jobs.
            That might be done via web interface
            Then, setups the tornado web server, you will need a local mongodb installation for this.
        """

        self.read_config()
        urls=[
                ("/([^/]+)", self.MainHandler),
                ("/", self.MainHandler),
                ("/new/([^/]+)", ObjectManager),
                ]

        settings=dict(
                #session_storage= 'mongodb:///tornado_sessions', # TODO Fix this.
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                xsrf_cookies=True,
                cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        )
        
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
        self.created_jobs=deque() # Don't delete, when views are created, they need a created_jobs argument in the creator. # TODO Make this use the queues
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
                slug=special_login_slugs[
                    
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
