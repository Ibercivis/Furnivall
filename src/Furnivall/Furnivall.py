from Core import *
from Plugins import *
from Views import *
from Core.common import CommonFunctions
import tornado.web
import tornado.ioloop


class ViewManager():
    def plug_view(self, viewfile, view):
        """
            Initialize a new job for a view and add it to job list.
            Check that there wasn't there before, as currently a view should only be executed once.
        """
        view=getattr(viewfile, view)()
        self.created_jobs.append({view.name : job(getattr(view.plugin, view.class_)()) })

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
        self.initialize_views=( getattr(viewfile, view)() for viewfile, view in self.config.options('enabled_views') )
        self.created_jobs=[ { view.name : job(getattr(view.plugin, view.class_)()) } for view in initialize_views ]

if __name__ == "__main__":
    """
        We call the tornado web server.
    """
    application = tornado.web.Application([(r"/", main),]) # Here we can setup, for example, the multiple views. launch a handler foreach view.
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
