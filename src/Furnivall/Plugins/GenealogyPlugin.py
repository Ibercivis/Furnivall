import logging, time

class GenealogyTree(object):
    def __init__(self):
        """
            Sample plugin, containing validation and consolidation functions
        """
        self.unique_name="GenealogyTreePlugin"
        self.description="Generate a collaborative genealogy tree"
        self.a = 0
        self.user = "" # TODO

    def task_executor(self, parent):
        parent.user_ = self.user # YUJU!
        while True:
            if parent.status == -2: 
                return # Wait for finish until someone changes its status.

    def validate_task(self, task, result):
        """
            Validate task.
        """
        if task.status == -2:
            return True # Always validate if user has said so, at least for the moment. We'll have to look at this later and probably make it event-based
        return -1 # This will be done in the web interface!

    def consolidate_result(self, results):
        """
            Make results consolidation for a workunit here.
        """
        return results

    def get_parent_nodes(self, task):
        try:
            raise(Exception("UnimplementedError"))
        except Exception, error:
            logging.info(error)
            return { '1' : ['3', '4'], '2' : ['3', '4'] }

    def add_node(self, node):
        # TODO: Get a free task and assign it this as result, and the user as parent.
        # We might need to add something else than a result to the task, but it's free so...
        return False

    def get_node_names(self, foo):
        try:
            raise(Exception("UnimplementedError"))
        except Exception, error:
            logging.info(error)
            return { '1' : 'Mom', '2' : 'Dad', '3' : 'Son', '4' : 'Dau' }
