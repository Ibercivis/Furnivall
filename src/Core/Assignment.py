#!/usr/bin/env python
import asyncore
from concurrent.futures import *
from collections import deque
from Personality import *
from Core.Tests import testclass
from tornado.options import options, define
from sqlalchemy import Column, Integuer, String
from sqlalchemy.ext.declarative import declarative_base


class Assignment()
    def __init__(self, creator_id, workunit_id, user__id):
        """
            Superclass of task and Result.
            @type creator_id: int
            @param creator_id: Id of the parent of this assignment 
            @type workunit_id: Id of the workunit this assignment was assigned to.
            @param user__id: Id of the user_ that got this assignment.
            @result: None.
        """
        self.creator=creator_id 
        self.workunit=workunit_id
        self.user_=user__id

    def append_to_creator(self, place, notification):
        """
            Append notification to Assignment object's creator' list. 

            Will get parent's list as specified in place argument and append
            notification.

            Should not produce output.
            @type place: string 
            @param place: queue object in the parent where we'll be storing notification 
            @type notification: string 
            @param notification: Object we'll add to parent place.
            @returns: None
            >>> b=WorkUnit() # TODO Fix this tests.
            >>> a=Assignment(creatorTest(),0,0) #doctest: +ELLIPSIS
            >>> a.append_to_creator('tasks','fooobar')
            >>> a.creator.tasks
            >>> # should be empty, as tasks are not executed synchronously
            >>> # (except for the foobar we just notified) NOTE: As this is
            >>> # not having control over the task time, MIGHT fail. )
            ['fooobar']
        
        """
        getattr(self.creator, place).append(notification)
        
class task(Assignment):
    def __init__(self, creator, workunit, user_, description):
        """
            Will launch as executor the *launch* function, wich is actually a
            call to job.pluginobject.launch_task. That will call the plugin
            to launch the task itself, all of it is made asynchronously.
            When created, it'll notify its creator that's been created,
            and, when finished, it'll validate it.

            TODO: by default task's assigning a user_, empty, change it to FALSE.'
            TODO: Right now this unit testing must be refactorished to use queues.

            >>> a=task(creatorTest(),[],[],"Task test")
            >>> a.description
            'Task test'
            >>> a.creator #doctest: +ELLIPSIS
            <__main__.creatorTest object at 0x...>
            >>> a.workunit
            []
            >>> a.user_
            []
            >>> a.creator.tasks #doctest: +ELLIPSIS
            [[<__main__.task object at 0x...>, <Future at 0x... state=finished returned NoneType>]]

        """
        super(task, self).__init__(creator, workunit, user_) # Initialize superclass. 
        self.description=description 
        MAX_WORKERS=20 # FIXME This has to be configurable!
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor: # Async call 
            self.futureobject=executor.submit(self.launch) 
            self.futureobject.add_done_callback(self.task_validator) # We validate it once it's done.
            self.append_to_creator('tasks',[self, self.futureobject]) # TODO: here we'll have, somehow to use ids too... Also, this futureobject must be checked out 
 
    def scoreMatch(self, user_): #surely not user_, but architecture or something so
        """
            Tells how adequate this task is for this user_.

            Returns 0 if the task can not be executed by the user_'s architecture. Else it returns
            a real between 0 and 1.

        """
        return 0

    def launch(self):
        """
            Produces asynchronously the Result.
            Once we have the Result (we can do whatever here, it's async...

            *Notes*

            - We've got to use "Result" object for that, creating a result object in plugin.launch_task.

            *Warns*

            - Result needs the reference to task the task to notify its creator

        """
        logging.info('\t\t\t[Debug] Asynchronous init for task %s\
                \n\t\t\t\t Parent %s \n\t\t\t\t Grandfather %s'
                %(self, self.workunit, self.creator.job))
        pluginObject=getattr(getattr(self.creator, "job"), self.pluginObject)
        pluginObject.launch_task(self) # This can be done like that in a futureObject

    def task_validator(self, futureObject): #this is a bad name, because in BOINC validation is a wider concep
        """
            Validates the task, calling the pluginObject's validate_task function.

            If task has passed, it'll append it to task_ok pool at it's creator, 
            otherwise in tasks_fail


        """
        passed=getattr(self.creator, "job").pluginObject.validate_task(self, futureObject)
        if passed:
            self.append_to_creator('tasks_ok', self)  
            # TODO: create a result here? Or from http service?
        else:
            self.append_to_creator('tasks_fail', self)  #quizas mejor self.creator.FailTask(self) ???

class Result(Assignment):
    def __init__(self, task, description):
        """
            Result object for a task.

            >>> workunit=WorkUnit()
            >>> a=task(creatorTest(),0,0,"Task test")
            >>> a.description
            'Task test'
            >>> b=Result(a,'result description')
            >>> b.creator #doctest: +ELLIPSIS
            <__main__.creatorTest object at 0x...>
            >>> b.workunit
            []
            >>> b.user_
            []
            >>> b.append_to_creator('tasks','fooobar')
            >>> b.creator.tasks #doctest: +ELLIPSIS
            [[<__main__.task object at 0x...>, <Future at 0x... state=finished returned NoneType>], 'fooobar']

        """
        
        super(Result, self).__init__(task.creator, task.workunit, task.user_)
        self.description=description 

    def Result_notification(self):
        """
            Notify task's creator itself to result (this will be called when task is finished).
            Then, call creator's consolidate_result function (wich probably will call this tasks's plugin
            consolidate_result function)
        """
        self.append_to_creator('results', self) # This adds to results deque in workunit this result object. 
        self.creator.consolidate_result()

class ConsolidatedResult(Result):
    def __init__(self, data, plugin):
        """
           Consolidated Result, data property returns inittialized data.
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
