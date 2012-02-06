import tornado.web

classes_to_append = [ "GenealogyView" ]
import logging 
class GenealogyView(object):
    def __init__(self, creator):
        """
            Genealogy view object. 
        """
        self.plugin = "GenealogyPlugin"
        self.class_ = "GenealogyTree"
        self.name = "Genealogy"
        self.description = "Genealogy View"
        self.workunits = 1 
        self.templates = {'Genealogy': ('GenealogyView', 'main_view')} 
        self.job = creator # TODO: pass job here.

    def get_task(self):
        """
            Must be called via RPC first, it will return a task location, wich will need to be used on all stuff
        """
        return

