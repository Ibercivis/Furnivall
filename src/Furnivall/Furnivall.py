from Core import *
import Plugins
from Plugins import *
import Views
from Views import *
from Core.common import CommonFunctions
import tornado.web
import tornado.ioloop
from Core.common import log
import Personality

class ViewManager(tornado.web.RequestHandler):
    def plug_view(self, viewfile, view):
        """
            Initialize a new job for a view and add it to job list.
            Check that there wasn't there before, as currently a view should only be executed once.
        """
        global created_jobs
        view=getattr(viewfile, view)()
        created_jobs.append({view.name : Jobs.job(getattr(view.plugin, view.class_)()) })

     def get(self, slug=False):
        if not slug:
            slug="Landing"
        log('[Debug] Rendering template %s' %slug)
        self.render('Templates/%s' %(slug), jobs=created_jobs, slug=slug )

        if self.get_argument('get_task'):
            self.assign_task(self.get_argument('view')) 

class main(CommonFunctions):
    def __init__(self):
        """
            Initializes jobs for each view
            Creates and provides a list of initialized jobs.
            This way we can have multiple plugins for one view.
        """
        global created_jobs
        created_jobs=[] # Don't delete, when views are created, they need a created_jobs argument in the creator.
        self.read_config()
        self.initialize_views=( getattr(getattr(Views, viewfile), self.conf('enabled_views', viewfile) )(self) for viewfile in self.config.options('enabled_views') )
        log('Loading Furnivall (Creating jobs)')
        created_jobs=[ { view.name : Jobs.job(view, getattr(getattr(Plugins, view.plugin), view.class_)()) } for view in self.initialize_views ]

    class Scheduler(ViewManager):
        """
            Assigns a volunteer a specific task
            WARN, NOTE: This might be loosing performance and scalability!
        """
        def assign_session_to_user(self, volunteer):
            return volunteer.set_data(self.session.host, self.session.user, self.session.session_id) # TODO Use real session data from the user.

        def assign_task(self, view):
            # TODO: check if the user is already doing that task?
            log('[Debug] Creating volunteer object and assigning it to a task.')
            assign_session_to_user(self.getfreetask(view).volunteer)

        def getworkunit(self):
            return WorkUnit.workunit() # TODO get workunit.

        def getfreetask(self, view):
            # TODO: change ScoreMatch in workunit to call the plugin/view's compatibility class. TODO: Make a view's compatibility class
            for job in created_jobs:
                for view, job in job:
                    if job.viewObject.check_view(volunteer): # Get volunteer object here! TODO
                        wk=self.getworkunit()
                        task=[sort(task, key=lambda t: t.ScoreMatch()) for task in wk.tasks if not task.volunteer.session_id ][0] # Get the best task ordered by ScoreMatch if it has not a volunteer assigned
                        if task: return task
                        else: return wk.new_task()
            return 

        def get_done_tasks(self):
            atasks=[]
            volunteer=self.get_volunteer(self.session)
            for workunit in self.find_volunteer_workunits(volunteer):
                atasks.extend([task in self.find_volunteer_tasks(volunteer, workunit.tasks_ok, workunit.tasks_fail)])
            return atasks

        def get_volunteer(self, session):
            # TODO Change the method volunteers work. Should be individual volunteers, by sessions, not by-task volunteers.
            return self.volunteers[session]

        def find_volunteer_workunits(self, volunteer):
            for job in created_jobs:
                for name, job in job:
                    for workunit in job.workunits:
                        if volunteer is workunit.volunteer: yield volunteer

        def find_volunteer_tasks(self, volunteer, tasks_ok, tasks_fail):
            tasks_ok.extend(tasks_fail)
            return [ task for task in tasks_ok if task.volunteer is volunteer ]

if __name__ == "__main__":
    """
        We call the tornado web server.
    """
    m=main()
    main_urls=("/view/([^/]+)", m.ViewManager)
    urls=[ b for b in [ a[a.keys()[0]].viewObject.urls for a in created_jobs ]][0]
    urls.append(main_urls)
    settings={'session_storage': 'mongodb:///tornado_sessions' }
    log('Starting web server with urls %s' %(urls))
    application = tornado.web.Application(urls, **settings) # Here we can setup, for example, the multiple views. launch a handler foreach view.
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
