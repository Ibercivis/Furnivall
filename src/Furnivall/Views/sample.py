import tornado.web
from Core.common import log

class SampleView(object):
    def __init__(self, creator):
        self.plugin="sample"
        self.class_="SamplePlugin"
        self.name="Sample_View"
        self.description="foo"
        self.workunits=30
        self.templates=['SampleView']
        self.urls=[( '/sample', creator.Scheduler ), ('/error', self.render_sample_view_external)] # Only scheduler can manage created jobs!

    class render_sample_view_external(tornado.web.RequestHandler):
        def get(self):
            self.render('../Templates/ExternalView.html')
