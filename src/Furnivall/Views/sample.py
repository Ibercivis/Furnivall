import tornado.web

classes_to_append = [ "SampleView" ]

class SampleView(object):
    """
        Sample view object. 

        Notes:

          - If you want a view acting like this one looks to act, you'll have to implement persistence (see below)
          - This one relys completly on plugin for the action.
        
    """
    def __init__(self, creator):

        self.plugin="sample" # Plugin file
        self.class_="SamplePlugin" # Plugin class (inside that file, so we can make multiple "plugins" from a plugin
        self.name="Sample_View" # View name
        self.description="Sample View" # View description
        self.workunits=3 # Initial workunits, this is the number of workunits that will be used.
        self.templates={'sample': 'SampleView'} # Templates for the web server.

    def do_stuff(object):
        return 
