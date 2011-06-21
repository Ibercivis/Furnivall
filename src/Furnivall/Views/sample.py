import tornado.web
from Core.common import log

class SampleView(object):
    def __init__(self, creator):
        """
            Sample view object.
        """
        self.plugin="sample" # Plugin file
        self.class_="SamplePlugin" # Plugin class (inside that file, so we can make multiple "plugins" from a plugin
        self.name="Sample_View" # View name
        self.description="Sample View" # View description
        self.workunits=3 # Initial workunits, this is the number of workunits that will be used.
        self.templates=['SampleView'] # Templates for the web server.
        self.urls=[( '/sample/', creator.Scheduler ), ('/error', self.render_sample_view_external)] # Only scheduler can manage created jobs!

    class render_sample_view_external(tornado.web.RequestHandler):
        def get(self):
            """
                Web requests will be made here, we can use get_argument to process data.
            """
            self.render('../Templates/ExternalView.html')

