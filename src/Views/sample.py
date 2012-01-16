import tornado.web

classes_to_append = [ "SampleView" ]

class SampleView(object):
    def __init__(self, creator):
        """
            Sample view object. 
            Notes:
            - If you want a view acting like this one looks to act, you'll have to implement persistence (see below)
            - This one relys completly on plugin for the action.
            
            *Persistence implementation*
            
            If you figure out any other way to do this, hell, do it!
            urls for tornado may not be inserted on plug time, so
            you'll have to add it on code, NOT HERE, in Furnivall.py's urls
            In a future, when persistence is implemented, you might
            be able to restart webserver (thus reloading the urls) and conserving all the objects.
            May be possible now, but it's risky and will probably fail.

        """
        self.plugin="sample" # Plugin file
        self.class_="SamplePlugin" # Plugin class (inside that file, so we can make multiple "plugins" from a plugin
        self.name="Sample_View" # View name
        self.description="Sample View" # View description
        self.workunits=3 # Initial workunits, this is the number of workunits that will be used.
        self.templates=['SampleView'] # Templates for the web server.
        self.urls=[( '/sample/', creator.MainHandler ), ('/error', self.render_sample_view_external)] # Only scheduler can manage created jobs!

    class render_sample_view_external(tornado.web.RequestHandler):
        def get(self):
            """
                Web requests will be made here, we can use get_argument to process data.
            """
            self.render('../templates/ExternalView.html')

