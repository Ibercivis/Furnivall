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

    def validate_task(self, result):
        """
            Validate task.
        """
        return True

    def consolidate_result(self, results):
        """
            Make results consolidation for a workunit here.
        """
        return results
