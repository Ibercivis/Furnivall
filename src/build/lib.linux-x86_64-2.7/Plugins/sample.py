class SamplePlugin(object):
    def __init__(self):
        """
            Sample plugin, containing validation and consolidation functions
        """
        self.description="Test plugin"
        self.user = ""

    def task_executor(self, parent):
        parent.user_ = self.user # YUJU!


    def validate_task(self, result, async):
        """
            Validate task.
        """
        return True

    def consolidate_result(self, results):
        """
            Make results consolidation for a workunit here.
        """
        return results
