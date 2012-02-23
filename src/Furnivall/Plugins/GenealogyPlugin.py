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
            return True # Always validate if user has said so, at least for the moment. We'll have to look at this later and probably make it event-based for the mail confirmation
        return -1 # This will be done in the web interface!

    def consolidate_result(self, results):
        """
            Make results consolidation for a workunit here.
        """
        return results

    def get_related_nodes(self, task):
        db = task.workunit.application.db
        for user in db['users']:
            for relationship in user['relationships']:
                if relationship[0] == task.user:
                    yield relationship

    def invert_relation(self, relation):
        rels = { 'cousin': 'cousin',
          'father': 'son' } # And now, wtf?
        return rels[relation]

    def search_for_identity(self, data):
        # With all data, return the closest match to an identity
        return "00000" # node

    def get_task_from_node(self, node):
        """
            Search on all job's workunits, if there's a task with that ID, return it.
            Otherwise, search in user's tasks in database, *this must not happen* but
            the task might have get lost!
        """
        try:
            for wk in task.workunit.job.workunits: # TODO check the path
                try:
                    return wk.tasks[node]
                except:
                    pass
            for user in task.application.db['users']:
                try:
                    return task.application.db['users'][user].tasks[node]
                except:
                    pass
            raise Exception("Could not find task")
        except Exception, warning:
            logging.debug(warning)
            return False

    def add_node(self, task, node, relation):
        """
            Gets the related node from get_task_from_node
            If it does not exist, it creates it // TODO: Add personal information here to the search.
            Then appends the relationship to both nodes, note that relationships are in english, just normal relationships words.
        """
        relation_task = self.get_task_from_node(node)
        if not relation_task:
            relation_task = task.workunit.job.get_task() # So, here we create a new task from inside a task.
        relation_task['relationships'].append([task.id_, invert_relation(relation)])
        task['relationships'].append([node, relation_task.id_])
        return True

    def get_node_names(self, task, foo):
        try:
            raise(Exception("UnimplementedError"))
        except Exception, error:
            logging.info(error)
            return { '1' : 'Mom', '2' : 'Dad', '3' : 'Son', '4' : 'Dau' }

    def get_parent_nodes(self, task):
        relationships = [ rel for rel in self.get_related_nodes(task) ] # We get relationships.
        try:
            raise(Exception("UnimplementedError"))
        except Exception, error:
            logging.info(error)
            return { '1' : ['3', '4'], '2' : ['3', '4'] }
