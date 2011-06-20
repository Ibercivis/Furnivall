"""
    Documentacion principal
    
"""

from Core import *
import Plugins
from Plugins import *
import Views
from Views import *
from Core.common import CommonFunctions
import tornado.web
import tornado.ioloop
from Core.common import log
import uuid

class ViewManager(tornado.web.RequestHandler):
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
        global created_jobs
        view=getattr(viewfile, view)()
        created_jobs.append({view.name : Jobs.job(getattr(view.plugin, view.class_)()) })

    def get(self, slug=False):
        """
            Tornado RequestHandler get function, renders slug as called 
            from tornado, passing jobs and slug as argument.
            It also checks arguments to take actions when arguments are provided
        """
        if not slug:
            slug="Landing"
        log('[Debug] Rendering template %s' %slug)
        self.render('Templates/%s' %(slug), jobs=created_jobs, slug=slug )

        if self.get_argument('get_task'):
            self.assign_task(self.get_argument('view')) 

class main(CommonFunctions):
    def __init__(self):
        """
            Creates a list of researchers, wich SHOULD (todo) contain jobs.
            That might be done via web interface
        """
        global created_jobs
        created_jobs=[] # Don't delete, when views are created, they need a created_jobs argument in the creator.
        self.read_config()

        log('Loading Furnivall (Creating jobs)')
        researchers=self.InitializeResearchers()

    def InitializeResearchers(self):
        " Initialize researchers, foreach researcher stored in database, recreate it"
        # Initially, this can be like this, as we've not implemented persistence yet'.
        return []

    class Scheduler(ViewManager):
        """
            Assigns a volunteer a specific task
            WARN, NOTE: This might be loosing performance and scalability!
        """

        def assign_session_to_user(self, volunteer):
            """
                Creates a unique session id and assigns it to volunteer object.
                then, it returns the volunteer with host and user data.
            """
            auuid=uuid.uuid4()
            self.session.user_id=auuid # Assign user id to session.
            log("[Debug Creating user %s,%s,%s" %(auuid, self.session.host, self.session.user))
            return volunteer.set_data(self.session.host, self.session.user, auuid )

        def assign_task(self, view):
            """
                Get a free task, if volunteer is doing that task, return an error, otherwise 
            """
            free_task=self.getfreetask()
            if get_current_volunteer() is free_task.volunteer: 
                log('[Debug] Not creating user, not return task... User is already doing that task, something failed!')
                return
            log('[Debug] Creating volunteer object and assigning it to a task.')
            assign_session_to_user(self.getfreetask(view).volunteer)

        def getworkunit(self):
            """
                Return a new workunit object.
            """
            log("Creating new workunit object")
            return WorkUnit.workunit() # TODO get workunit.

        def get_current_volunteer(self):
            """
                Get current volunteer, by session id (session_id is scheduler-specific, should be for each user)
                If no session_id, calls assign_session_to_user
            """
            if not self.session.session_id:
                return assign_session_to_user
            else:
                log('Getting volunteer object for id: %s' %(self.session.session_id))
                return self.volunteers[self.session.session_id] # FIXME Make volunteers pool!!!

        def getfreetask(self, view):
            """
                If user is able to execute a determinated view task, get a workunit and return the task
                with better score, and with no session_id.
                If user is able to execute the task, but no pre-created (and not assigned) tasks are available, return a new task.
                Should iterate trough a researcher pool, getting jobs, then split jobs in view, job, and check view's compatibility.
                
            """
            # TODO: change ScoreMatch in workunit to call the plugin/view's compatibility class. TODO: Make a view's compatibility class
            for researcher in researchers:
                for job in researcher.jobs:
                    for view, job in job:
                        if job.viewObject.check_view(get_current_volunteer):
                            wk=self.getworkunit()
                            task=[sort(task, key=lambda t: t.ScoreMatch()) for task in wk.tasks if not task.volunteer.session_id ][0] # Get the best task ordered by ScoreMatch if it has not a volunteer assigned
                            if task: return task
                            else: return wk.new_task()
            return 

        def get_done_tasks(self):
            """
                Return tasks in status "ok" and "failed" from a volunteer's tasks_fail and tasks_ok pools.
            """
            atasks=[]
            volunteer=self.get_current_volunteer()
            for workunit in self.find_volunteer_workunits(volunteer):
                atasks.extend([task in self.find_volunteer_tasks(volunteer, workunit.tasks_ok, workunit.tasks_fail)])
            return atasks

        def find_volunteer_workunits(self, volunteer):
            """
                Generator returning volunteer workunits. Warning: this might be dangerous, as we've seen that
                generators seem to not work Ok when removing elements from its object.
            """
            for researcher in researchers: # TODO Make researchers pool, and make it global! Then check everywhere when it's changed
                for job in researcher.jobs:
                    for name, job in job:
                        for workunit in job.workunits:
                            if volunteer is workunit.volunteer: yield volunteer

        def find_volunteer_tasks(self, volunteer, tasks_ok, tasks_fail):
            """
                return tasks from tasks_ok and task_fail if they're from volunteer
            """
            tasks_ok.extend(tasks_fail)
            return [ task for task in tasks_ok if task.volunteer is volunteer ]

if __name__ == "__main__":
    """
        Setup the tornado web server
    """
    m=main()
    main_urls=("/view/([^/]+)", m.Scheduler)
    try:
        urls=[ b for b in [ a[a.keys()[0]].viewObject.urls for a in created_jobs ]][0]
    except:
        urls=[] # FIXME This should not happen should'nt it?
    urls.append(main_urls)
    settings={'session_storage': 'mongodb:///tornado_sessions' } # FIXME Document installation and configuration.
    log('Starting web server with urls %s' %(urls))
    application = tornado.web.Application(urls, **settings) # Here we can setup, for example, the multiple views. launch a handler foreach view.
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
