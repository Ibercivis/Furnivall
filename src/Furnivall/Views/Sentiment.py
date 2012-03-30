import tornado.web

classes_to_append = [ "SentimentView" ]
import logging 
class SentimentView(object):
    def __init__(self, creator):
        """
            Sentiment view object. 
        """
        self.plugin = "SentimentPlugin"
        self.class_ = "SentimentAnalysis"
        self.name = "Sentiment"
        self.description = "Sentiment View"
        self.workunits = 1 
        self.templates = {'Sentiment': ('SentimentView', 'main_view')} 
        self.job = creator # TODO: pass job here.

    def get_or_create_task(self):
        """
            Must be called via RPC first, it will return a task location, wich will need to be used on all stuff
        """
        logging.info("FOO");
        return

    def get_task(self):
        """
            Must be called via RPC first, it will return a task location, wich will need to be used on all stuff
        """
        logging.info("FOO");
        return

