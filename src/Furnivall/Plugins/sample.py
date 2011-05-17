class SamplePlugin(object):
    def __init__(self):
        self.description="Test plugin"

    def validate_task(self, result, async):
        return True
