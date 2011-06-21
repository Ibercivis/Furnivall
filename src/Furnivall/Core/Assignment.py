#!/usr/bin/env python
import asyncore
from concurrent.futures import *
from collections import deque
from Personality import *
from Core.common import log
from Core.Tests import testclass

class plugintest(testclass):
    def __init__(self):
        self.workunits=10
        self.pluginmodule=Tests
        self.pluginclass="testclass"
        self.description="foobar"

    def main(self):
        return "foo" 

class Assignment(object):
    def __init__(self, creator, workunit, volunteer):
        """
            Superclass of task and Result
            >>> a=Assignment(Job(viewtest, plugintest),[],[])
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
            TODO: by default task's assigning a volunteer, empty, change it to FALSE.'
            It will launch as executor the launch function, wich is actually a call to job.pluginobject.launch_task
            So, basically this is calling the plugin to launch the task itself, asyncrounously via TrheadPoolExecutor
            When created, it'll notify its creator that's been created, and, when finished, it'll validate it.'

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
            self.futureobject=executor.submit(self.launch) 
            self.futureobject.add_done_callback(self.task_validator) # We validate it once it's done.
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
        log('\t\t\t[Debug] Asynchronous init for task %s \n\t\t\t\t Parent %s \n\t\t\t\t Grandfather %s' %(self, self.workunit, self.creator.job))
        return getattr(getattr(self.creator, "job"), self.pluginObject).launch_task(self) # This can be done like that in a futureObject
        # Maybe more readable with self.creator.job.pluginObject.launch_task(self) ?? Or even worse?
        # It's a way to have each job with a different launch function (Result producer)
        # Note we've got to use "Result" object for that, creating a result object in plugin.launch_task.
        # Warn: Result needs the reference to task!!


    def task_validator(self, futureObject): #this is a bad name, because in BOINC validation is a wider concep
        """
            Validates the task, calling the pluginObject's validate_task function.
            If task has passed, it'll append it to task_ok pool at it's creator, 
            otherwise in tasks_fail
        """
        passed=getattr(self.creator, "job").pluginObject.validate_task(self, futureObject)
        if passed:
            self.notify_creator('tasks_ok', self)  
            # TODO: create a result here? Or from http service?
        else:
            self.notify_creator('tasks_fail', self)  #quizas mejor self.creator.FailTask(self) ???

class Result(Assignment):
    def __init__(self, task, description):
        """
            Result object for a task.
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
        """
            Notify task's creator itself to result (this will be called when task is finished).
            Then, call creator's consolidate_result function (wich probably will call this tasks's plugin
            consolidate_result function)
        """
        self.notify_creator('results', self) # This adds to results deque in workunit this result object. 
        self.creator.consolidate_result()

class ConsolidatedResult(Result):
    def __init__(self, data, plugin):
        """
           consolidated Result, data property returns inittialized data.
        """
        self.data=plugin.consolidate_result(data)

    @property
    def data(self):
        return self.data

if __name__ == "__main__":
    """
        This should never be used as standalone but for unittests
    """
    import doctest
    from Jobs import *
    from Tests import *
    doctest.testmod()
