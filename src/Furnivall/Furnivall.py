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
        view=getattr(viewfile, view)()
        self.created_jobs.append({view.name : Jobs.job(getattr(view.plugin, view.class_)()) })

class Scheduler(tornado.web.RequestHandler, ViewManager):
    def get(self):
        if not self.get_argument('return_data'): 
            if self.get_argument('view'):
                if not self.created_jobs[self.get_argument['view']]:
                    self.plug_view(self.get_argument("viewfile"), self.get_argument("view"))
        else:
            return pickle(self.created_jobs[self.get_argument('view')])

class main(CommonFunctions, Scheduler):
    def __init__(self):
        """
            Initializes jobs for each view
            Creates and provides a list of initialized jobs.
            This way we can have multiple plugins for one view.
        """
        log('Starting furnivall, reading config')
        self.read_config()
        log('Creating views generator (should be instant)')
        self.initialize_views=( getattr(getattr(Views, viewfile), self.conf('enabled_views', viewfile) )() for viewfile in self.config.options('enabled_views') ) # FIXME That's not the correct way to access view
        log('Creating jobs (may take a while) (If log enabled, you\'ll see a lot output now)')
        self.created_jobs=[ { view.name : Jobs.job(view, getattr(getattr(Plugins, view.plugin), view.class_)()) } for view in self.initialize_views ]

if __name__ == "__main__":
    """
        We call the tornado web server.
    """
    m=main()
    log('Extracting URLs from views already created.')
    urls=[ a[a.keys()[0]].viewObject.urls for a in m.created_jobs ]

    log('Starting web server')
    application = tornado.web.Application(urls) # Here we can setup, for example, the multiple views. launch a handler foreach view.
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
