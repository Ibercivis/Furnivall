class testclass():
    def __init__(self):
        """
            Base class for all Tests
        """
        self.a="foo"

class creatorTest(testclass):
    def __init__(self):
        """
            Provides a fake creator class that will act as job or workunit.
        """
        self.tasks=[]
        self.tasks_ok=[]
        self.tasks_fail=[]
        self.creator=self

    def validate_task(self, task, futureobject):
        """
            Fake validator that validates all tasks as ok
        """
        return True

    def consolidate_result(self, result):
        """
            Fake consolidtaror that returns result itself as ConsolidatedResult
        """
        return result

class viewtest(testclass):
    def __init__(testclass):
        """
            Fake view object
        """
        self.workunits=10
        self.pluginmodule=Tests
        self.pluginclass="testclass"
        self.description="foobar"

    def main(self):
        """
            Return foo as result
        """
        return "foo" 

    def validate_task(self, foo, bar):
        """
            Secondary task validator for tests, can override plugin's one
        """

        return True
