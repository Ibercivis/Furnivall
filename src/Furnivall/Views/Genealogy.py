import tornado.web

classes_to_append = [ "GenealogyView" ]

class GenealogyView(object):
    def __init__(self, creator):
        """
            Genealogy view object. 
            Notes:
            - If you want a view acting like this one looks to act, you'll have to implement persistence (see below)
            - This one relys completly on plugin for the action.
p

            When /view/{{researcher}}/Genealogy/ has ben called, we call GenealogyView.main_view, remember to put / at the end. This is because it will support having ONE slug (/foo), wich can be, for example, 
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
