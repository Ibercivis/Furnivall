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
        self.creator=self

    def validate_task(self, task, futureobject):
        return True

    def consolidate_result(self, result):
        return True

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
            >>> a.creator.tasks 
            >>> # should be empty, as tasks are not executed synchronously
            >>> # (except for the foobar we just notified) NOTE: As this is
            >>> # not having control over the task time, MIGHT fail. )
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
        super(task, self).__init__(creator, workunit, volunteer) # Initialize superclass. 
        self.description=description 
        MAX_WORKERS=20 # FIXME This has to be configurable!
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor: # Async call 
            # Launch as executor launch function, wich will be a call to job.pluginobject.launch_task
            # So, basically this is calling the plugin to get it's
            self.futureobject=executor.submit(self.launch) 
            self.futureobject.add_done_callback(self.task_validator) # We validate it once it's done.
            # We send to the creator (workunit)'s task list, the futureobject and the task itself
            self.notify_creator('tasks',[self, self.futureobject])
 
    def scoreMatch(self, volunteer): #surely not volunteer, but architecture or something so
        """
            Tells how adequate this task is for this volunteer.
            Returns 0 if the task can not be executed by the volunteer's architecture. Else it returns
            a real between 0 and 1.
            (See also task_validator???)
        """
        return 0

    def launch(self):
        """
            Produces asynchronously the Result.
            Once we have the Result (we can do whatever here, it's async...
        """
        # return getattr(getattr(self.creator, "job"), pluginObject).launch_task(self) # This can be done like that in a futureObject
        # Maybe more readable with self.creator.job.pluginObject.launch_task(self) ?? Or even worse?
        # It's a way to have each job with a different launch function (Result producer)
        # Note we've got to use "Result" object for that.
        return

    def task_validator(self, futureObject): #this is a bad name, because in BOINC validation is a wider concept
        passed=getattr(self.creator,"creator").validate_task(self, futureObject)
        if passed:
            self.notify_creator('tasks_ok', self)  
            #create a result here? Or from http service?
        else:
            self.notify_creator('tasks_fail', self)  #quizas mejor self.creator.FailTask(self) ???

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
         self.creator.consolidate_result()

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
