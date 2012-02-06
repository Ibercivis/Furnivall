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
        self.name = "Genealogy_View"
        self.description = "Genealogy View"
        self.workunits = 1 
        self.templates = {'Genealogy': ('GenealogyView', 'main_view')} 
        self.creator = creator

    def main_view(self, slug):
        return "FOO"

    def get_parent_nodes(self, foo):
        try:
            raise(Exception("UnimplementedError"))
        except Exception, error:
            logging.info(error)
            return { '1' : ['3', '4'], '2' : ['3', '4'] }

    def add_node(self, node):
        # TODO: Get a free task and assign it this as result, and the user as parent.
        # We might need to add something else than a result to the task, but it's free so...


    def get_node_names(self, foo):
        try:
            raise(Exception("UnimplementedError"))
        except Exception, error:
            logging.info(error)
            return { '1' : 'Mom', '2' : 'Dad', '3' : 'Son', '4' : 'Dau' }
