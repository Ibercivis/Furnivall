from Core import *
from Plugins import *
from Views import *
from Core.common import CommonFunctions
class main(CommonFunctions):
    def __init__(self):
        self.initialize_views=( getattr(viewfile, view)() for viewfile, view in self.config.options('enabled_views') )
        self.created_jobs=[ job(getattr(view.plugin, view.class_)()) for view in initialize_views ]
            # Ok, so here we have:
            # job(view) where will be stored view stuff (so instead of enabled_plugins it's enabled_views now)
            # View will have to specify the plugin, so we'll initialize it in the job.
            # This way we can have one plugin for multiple views, so we can make different user interfaces for one single purpose
        # Initialize view http servers???
            
