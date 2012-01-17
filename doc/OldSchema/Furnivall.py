from furnivall.core import *

#from furnivall.plugins import *


class FurnivallLoader():
    """
       TODO: Import only active plugins, make it via conffile, conffile accesible via API.
    """
    def __init__(self):
        return self.load_plugins(config_read(CONFFILE))

    def load_plugins():
        return 

class FurnivallServer():
    """
        TCP Server, exporting API.
    """
    self.async_server
    self.api_exporter


