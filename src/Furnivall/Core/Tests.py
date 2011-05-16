import Tests
class testclass():
    def __init__(self):
        self.a="foo"

class creatorTest(object):
    def __init__(self):
        self.tasks=[]
        self.tasks_ok=[]
        self.tasks_fail=[]
        self.creator=self

    def validate_task(self, task, futureobject):
        return True

    def consolidate_result(self, result):
        return True

class viewtest():
    def __init__(self):
        self.workunits=10
        self.pluginmodule=Tests
        self.pluginclass="testclass"
        self.description="foobar"

    def main(self):
        return "foo" 

    def validate_task(self, foo, bar):
        return True
