class testclass():
    def __init__(self):
        self.a="foo"

class creatorTest(testclass):
    def __init__(self):
        self.tasks=[]
        self.tasks_ok=[]
        self.tasks_fail=[]
        self.creator=self

    def validate_task(self, task, futureobject):
        return True

    def consolidate_result(self, result):
        return True

class viewtest(testclass):
    def __init__(testclass):
        self.workunits=10
        self.pluginmodule=Tests
        self.pluginclass="testclass"
        self.description="foobar"

    def main(self):
        return "foo" 

    def validate_task(self, foo, bar):
        return True
