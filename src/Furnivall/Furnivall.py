from Core import *
from Plugins import *
from Core.common import CommonFunctions
class main(CommonFunctions):
    def __init__(self):
        # We've got all in the core, but nothing about the views nor plugin support really implemented!!!
        # Ok, so we launch a workunit foreach stuff we've got configured for, with the plugin callable foreach stuff 
        # Still unimplemented:
        # Way to 
        self.created_jobs=[ job(getattr(plugin, class_)()) for plugin, class_ in\
                self.config.options('enabled_plugins') ]
        # Initialize view http servers???
            
