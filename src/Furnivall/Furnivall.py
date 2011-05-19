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
            log('[Debug] [Scheduler] Launched to %s' %slug)
            self.render('Templates/%s' %(slug), jobs=created_jobs, slug=slug )
            # NOTE: You can do more things. We've got here access to the views' initialized object =)

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
            TODO: Call this from somwhere
        """
        def assign_task(self):
            # Lets see... volunteer == host?
            # We should get a unique session id for it from the webserver (tornado).
            # Hell, tornado itself doesnt store sessions!!!!
            # That makes it impossible to use it for this... unless... hey! =D A fork! With session support!
            # https://github.com/milancermak/tornado
            # Then create a volunteer job.
            v=Personality.Volunteer()
            # And now get that volunteer into a specific task...
            self.getn_freeTask().volunteer.id=get_id_from_server()

if __name__ == "__main__":
    """
        We call the tornado web server.
    """
    m=main()
    main_urls=("/view/([^/]+)", m.Scheduler)
    urls=[ b for b in [ a[a.keys()[0]].viewObject.urls for a in created_jobs ]][0]
    urls.append(main_urls)
    settings={'session_storage': 'mongodb:///tornado_sessions' }
    log('Starting web server with urls %s' %(urls))
    application = tornado.web.Application(urls, **settings) # Here we can setup, for example, the multiple views. launch a handler foreach view.
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
