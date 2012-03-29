import logging, time

class SentimentAnalysis(object):
    def __init__(self):
        """
            Sample plugin, containing validation and consolidation functions
        """
        self.unique_name="SentimentAnalysis plugin"
        self.description="Generate a sentiment corpus"
        self.a = 0
        self.user = "" # TODO

    def task_executor(self, parent):
        parent.user_ = self.user # YUJU!

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

    def get_task(self, node):
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
