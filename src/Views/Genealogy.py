import tornado.web

classes_to_append = [ "GenealogyView" ]

class GenealogyView(object):
    def __init__(self, creator):
        """
            Genealogy view object. 
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
        self.plugin = "GenealogyPlugin"
        self.class_ = "GenealogyTree"
        self.name = "Genealogy_View"
        self.description = "Genealogy View"
        self.workunits = 1 
        self.templates = {'Genealogy': 'GenealogyView'}
