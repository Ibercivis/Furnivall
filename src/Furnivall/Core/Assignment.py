#!/usr/bin/env python
import asyncore
from concurrent.futures import *
from collections import deque
from Personality import *

class creatorTest(object):
    def __init__(self):
        self.tasks=[]
        self.tasks_ok=[]
        self.tasks_fail=[]

class Assignment(object):
    def __init__(self, creator, workunit, volunteer):
        """
            Assignment: superclass of task and Result
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
            # concurrent.futures.wait(fs, timeout=None, return_when=ALL_COMPLETED) --> This might be interesting for workunits
            self.futureobject=executor.submit(self.launch) 
            self.futureobject.add_done_callback(self.task_validator) # We validate it once it's done.
            self.notify_creator('tasks',[self, self.futureobject])

    def launch(self):
        """
            Produces asynchronously the Result.
            Once we have the Result (we can do whatever here, it's async...
        """
        # return getattr(self.creator).launch_task(self) # This can be done like that in a futureObject
        # It's a way to have each job with a different launch function (Result producer)
        # Note we've got to use "Result" object for that.
        return

    def task_validator(self, futureObject):
        passed=getattr(self.creator,"creator").validate_task(self, futureObject)
        if passed:
            self.notify_creator('tasks_ok', self)
        else:
            self.notify_creator('tasks_fail', self)

class Result(Assignment):
    def __init__(self, task, description):
        """
            Result of a task, having assignment + a description
            >>> a=task(creatorTest(),[],[],"Task test")
            >>> a.description
            'Task test'
            >>> b=Result(a,'result description')
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
        
        super(Result, self).__init__(task.creator, task.workunit, task.volunteer)
        self.description=description 

    def Result_notification(self):
         self.notify_creator('results', self) # This adds to results deque in workunit this result object.

class ConsolidatedResult(Result):
    def __init__(self, data):
        """
           consolidated Result, data property returns inittialized data.
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
