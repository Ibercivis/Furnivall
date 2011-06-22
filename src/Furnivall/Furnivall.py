"""
    Ibervicis Furnivall is an open source framework for distributed volunteer science.
    It helps to organize batches of tasks, collect them form volunteers and do all the related housekeeping.
"""

from Plugins import *
from Views import *
import Core.Assignment
import Core.WorkUnit
import Core.Personality 
import Core.common as common
import Plugins
import Views
import tornado.web
import tornado.ioloop
import tornado.httpserver
import uuid, os, logging
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class Scheduler(tornado.web.RequestHandler):
    def assign_session_to_user(self, volunteer):
        """
            Creates a unique session id and assigns it to volunteer object.
            then, it returns the volunteer with host and user data.
        """
        auuid=uuid.uuid4()
        self.session.user_id=auuid # Assign user id to session.
        logging.info("Creating user %s,%s,%s" %(auuid, self.session.host, self.session.user))
        return volunteer.set_data(self.session.host, self.session.user, auuid )

    def assign_task(self, view):
        """
            Get a free task, if volunteer is doing that task, return an error, otherwise 
        """
        free_task=self.getfreetask()
        if get_current_volunteer() is free_task.volunteer: 
            logging.info('[Debug] Not creating user, not return task... User is already doing that task, something failed!')
            return
        logging.info('[Debug] Creating volunteer object and assigning it to a task.')
        assign_session_to_user(self.getfreetask(view).volunteer)

    def getworkunit(self):
        """
            Return a workunit object, a new one if no unnasigned workunits available
        """
        for i in researcher.jobs.workunits:
            logging.info('Trying to return a free workunit. Currently processing %s' %(i))
            if not i.status:
                logging.info('%s is free!' %i)
                return i
        logging.info("Creating new workunit object")
        return researcher.jobs.produce_workunits()

    def get_current_volunteer(self):
        """
            Get current volunteer, by session id (session_id is scheduler-specific, should be for each user)
            If no session_id, calls assign_session_to_user
        """
        if not self.session.session_id:
            return assign_session_to_user
        else:
            logging.info('Getting volunteer object for id: %s' %(self.session.session_id))
            return self.volunteers[self.session.session_id] # FIXME Make volunteers pool!!!

    def getfreetask(self, view):
        """
            If user is able to execute a determinated view task, get a workunit and return the task
            with better scommon, and with no session_id.
            If user is able to execute the task, but no pre-created (and not assigned) tasks are available, return a new task.
            Should iterate trough a researcher pool, getting jobs, then split jobs in view, job, and check view's compatibility.
            
        """
        # TODO: change ScommonMatch in workunit to call the plugin/view's compatibility class. TODO: Make a view's compatibility class
        for researcher in self.application.researchers:
            logging.info('Processing researcher %s' %researcher)
            for job in researcher.jobs:
                logging.info('Processing job %s' %job)
                for view, job in job:
                    logging.info('Processing view and job %s %s' %(view, job))
                    if job.viewObject.check_view(self.get_current_volunteer()):
                        logging.info("View is supported by user (ViewOjbect: %s) (Volunteer: %s)" %(job.viewObject, self.get_current_volunteer()))
                        wk=self.getworkunit()
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
        logging.info('Getting done tasks for volunteer: %s' %volunteer)
        for workunit in self.find_volunteer_workunits(volunteer):
            atasks.extend([task in self.find_volunteer_tasks(volunteer, workunit.tasks_ok, workunit.tasks_fail)])
        logging.info('got %s' %atasks)
        return atasks

    def find_volunteer_workunits(self, volunteer):
        """
            Generator returning volunteer workunits. Warning: this might be dangerous, as we've seen that
            generators seem to not work Ok when removing elements from its object.
        """
        logging.info('Getting workunits for volunteer: %s' %volunteer)
        for researcher in self.application.researchers: # TODO Make researchers pool, and make it global! Then check everywhere when it's changed
            for job in researcher.jobs:
                for name, job in job:
                    for workunit in job.workunits:
                        if volunteer is workunit.volunteer: yield volunteer

    def find_volunteer_tasks(self, volunteer, tasks_ok, tasks_fail):
        """
            return tasks from tasks_ok and task_fail if they're from volunteer
        """
        logging.info('Getting all tasks for volunteer %s' %volunteer)
        tasks_ok.extend(tasks_fail)
        return [ task for task in tasks_ok if task.volunteer is volunteer ]

class ViewManager(Scheduler):
    """
        ViewManager Object, inherits tornado's requesthandler and provides
        the hability to plug a view into created_jobs list.
        Note that created_jobs has a dict foreach real job in the form
            { view.name : Jobs.job(<view.plugin.class object>) }
        that should be changed in a future for a []
    """

    def plug_view(self, viewfile, view):
        """
            Initialize a new job for a view and add it to job list.
            Check that there wasn't there before, as currently a view should only be executed once.
        """
        logging.info('Pluging view  %s: %s' %(viewfile, view))

        view=getattr(viewfile, view)()
        job={view.name : Jobs.job(getattr(view.plugin, view.class_)()) }
        logging.info('Created job: %s' %job)
        
        self.application.created_jobs.append(job)

    def get(self, slug=False):
        """
            Tornado RequestHandler get function, renders slug as called 
            from tornado, passing jobs and slug as argument.
            It also checks arguments to take actions when arguments are provided
        """
        if not slug:
            slug="Landing"
        logging.info('[Debug] Rendering template %s' %slug)
        self.render('%s' %(slug), jobs=self.application.created_jobs, researchers=self.application.researchers, slug=slug )
        try:
            if self.get_argument('get_task'):
                self.assign_task(self.get_argument('view')) 
        except:
            pass

class Application(common.CommonFunctions, tornado.web.Application):
    def __init__(self):
        """
            Creates a list of researchers, wich SHOULD (todo) contain jobs.
            That might be done via web interface
            Then, setups the tornado web server, you will need a local mongodb installation for this.
        """
        self.created_jobs=[] # Don't delete, when views are created, they need a created_jobs argument in the creator.
        self.read_config()

        logging.info('Loading Furnival')
        self.researchers=self.InitializeResearchers()
        logging.info('Researchers initialized by default: %s' %self.researchers)
        main_urls=("/view/([^/]+)", ViewManager)

        try:
            urls=[ b for b in [ a[a.keys()[0]].viewObject.urls for a in self.created_jobs ]][0]
        except:
            urls=[] # FIXME This should not happen should'nt it?

        urls.append(main_urls)

        logging.info('Starting server with urls: %s' %urls)

        settings=dict(
                #session_storage= 'mongodb:///tornado_sessions',
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                xsrf_cookies=True,
                cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        )
        
        tornado.web.Application.__init__(self, urls, **settings)



    def InitializeResearchers(self):
        """
            Initialize researchers, foreach researcher stored in database, recreate it
            Actually, it's returning an empty set, as persistence is not implemented.
        """
        # Initially, this can be like this, as we've not implemented persistence yet'.
        return []

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
