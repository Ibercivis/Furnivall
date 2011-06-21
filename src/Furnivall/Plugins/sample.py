class SamplePlugin(object):
    def __init__(self):
        """
            Sample plugin, containing validation and consolidation functions
        """
        self.description="Test plugin"


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
