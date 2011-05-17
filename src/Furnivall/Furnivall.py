from Core import *
import Plugins
from Plugins import *
import Views
from Views import *
from Core.common import CommonFunctions
import tornado.web
import tornado.ioloop
from Core.common import log


class ViewManager():
    def plug_view(self, viewfile, view):
        """
            Initialize a new job for a view and add it to job list.
            Check that there wasn't there before, as currently a view should only be executed once.
        """
        global created_jobs
        view=getattr(viewfile, view)()
        created_jobs.append({view.name : Jobs.job(getattr(view.plugin, view.class_)()) })


class main(CommonFunctions):
    def __init__(self):
        """
            Initializes jobs for each view
            Creates and provides a list of initialized jobs.
            This way we can have multiple plugins for one view.
        """
        global created_jobs
        created_jobs=[] # Don't delete, when views are created, they need a created_jobs argument in the creator.
        log('Starting furnivall, reading config')
        self.read_config()
        log('Creating views generator (should be instant)')
        self.initialize_views=( getattr(getattr(Views, viewfile), self.conf('enabled_views', viewfile) )(self) for viewfile in self.config.options('enabled_views') ) # FIXME That's not the correct way to access view
        log('Creating jobs (may take a while) (If log enabled, you\'ll see a lot output now)')
        created_jobs=[ { view.name : Jobs.job(view, getattr(getattr(Plugins, view.plugin), view.class_)()) } for view in self.initialize_views ]

    class Scheduler(tornado.web.RequestHandler, ViewManager):
        def get(self, slug=False):
            log('Scheduler launched to %s' %slug)
            log('Trying to render argument %s' %(slug))
            self.render('Templates/%s' %(slug), jobs=created_jobs )
            # TODO: Do more things. We've got here accesso to the views' initialized object =)

if __name__ == "__main__":
    """
        We call the tornado web server.
    """
    m=main()
    main_urls=("/view/([^/]+)", m.Scheduler)
    urls=[ b for b in [ a[a.keys()[0]].viewObject.urls for a in created_jobs ]][0]
    urls.append(main_urls)
    log('Starting web server with urls %s' %(urls))
    application = tornado.web.Application(urls) # Here we can setup, for example, the multiple views. launch a handler foreach view.
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
