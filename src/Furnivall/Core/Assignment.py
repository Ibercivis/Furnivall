#!/usr/bin/env python
import asyncore
from concurrent.futures import *

class creatorTest(object):
    def __init__(self):
        self.tasks=[]

class Assignment(object, asyncore.dispatcher):
    def __init__(self, creator, workunit, volunteer):
        """
            Assignment: superclass of task and result
            >>> a=Assignment(creatorTest(),[],[])
        """
        self.creator=creator
        self.workunit=workunit
        self.volunteer=volunteer

    def notify_creator(self, place, notification):
        """
            Notify creator object appending it to "place"
            >>> a=Assignment(creatorTest(),[],[]) #doctest: +ELLIPSIS
            >>> a.notify_creator('tasks','fooobar')
            >>> a.creator.tasks # should be empty, as tasks are not executed synchronously (except for the foobar we just notified)
            ['fooobar']
        
        """
        getattr(self.creator, place).append(notification)
        
class task(Assignment):
    def __init__(self, creator, workunit, volunteer, description):
        """
            Task object, having assignment + a description
            >>> a=task(creatorTest(),[],[],"Task test")
            >>> a.description
            'Task test'
            >>> a.creator #doctest: +ELLIPSIS
            <__main__.creatorTest object at 0x...>
            >>> a.workunit
            []
            >>> a.volunteer
            []
            >>> a.creator.tasks #doctest: +ELLIPSIS
            [[<__main__.task object at 0x...>, <Future at 0x... state=finished returned NoneType>]]

        """
        super(task, self).__init__(creator, workunit, volunteer) 
        self.description=description
        with ThreadPoolExecutor(max_workers=1) as executor:
            # concurrent.futures.wait(fs, timeout=None, return_when=ALL_COMPLETED) --> This might be interesting
            self.futureobject=executor.submit(self.launch) 
            self.futureobject.add_done_callback(self.task_validator) # We validate it once it's done.
            self.notify_creator('tasks',[self, self.futureobject])

    def launch(self):
        """
            Produces asynchronously the result.
            Once we have the result (we can do whatever here, it's async...
        """

        return

    def task_validator(self):
        # TODO Do validate checks here
        passed=True
        if passed:
            self.notify_creator('tasks_ok', self)
        else:
            self.notify_creator('tasks_fail', self)

class result(Assignment):
    def __init__(self, task, description):
        """
            result of a task, having assignment + a description
            >>> a=task(creatorTest(),[],[],"Task test")
            >>> a.description
            'Task test'
            >>> b=result(a,'result description')
            >>> b.creator #doctest: +ELLIPSIS
            <__main__.creatorTest object at 0x...>
            >>> b.workunit
            []
            >>> b.volunteer
            []
            >>> b.notify_creator('tasks','fooobar')
            >>> b.creator.tasks #doctest: +ELLIPSIS
            [[<__main__.task object at 0x...>, <Future at 0x... state=finished returned NoneType>], 'fooobar']

        """
        
        super(result, self).__init__(task.creator, task.workunit, task.volunteer)
        self.description=description 

    def result_notification(self):
        self.notify_creator('results', self)

class Volunteer(object):
    def __init__(self, host=False, user=False):
        self.host=host
        self.user=user

class Researcher(object):
    def __init__(self, host, user):
        self.host=host
        self.user=user
        self.jobs=[]

class ConsolidatedResult(object):
    def __init__(self, data):
        """
           consolidated result, data property returns inittialized data.
        """
        self.data=data

    @property
    def data(self):
        return self.data

if __name__ == "__main__":
    """
        This should never be used as standalone but for unittests
    """
    import doctest
    doctest.testmod()
