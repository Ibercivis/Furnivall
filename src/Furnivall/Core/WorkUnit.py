#!/usr/bin/env python
from collections import deque
from Assignment import *
from Core.common import log
class workunit(object):
    def __init__(self, job=False):
        """
            Simple job unit.
        """
        self.job=job
        self.tasks=deque()
        self.tasks_ok=deque()
        self.tasks_fail=deque()
        self.expected=0 #TODO this should get workunit expected tasks to return.
        self.results=deque()
        log('Producing %s tasks for workunit %s' %(job.initial_tasks, self))
        for i in range(0, int(job.initial_tasks)): self.new_task()

    def consolidate_result(self):
        if self.status:
            cr=self.results # TODO Consolidate result here.
            self.ConsolidatedResult=ConsolidatedResult(cr)
        # What about making this one assignment's child too and notify "job" 
        # (creator) with notify_creator when it's got a consolidated result?

    def task_ok(self, task_id):
        """
            append a task id to ok tasks.
            >>> a=workunit()
            >>> a.task_ok('123')
            >>> a.tasks_ok
            deque(['123'])
        """
        self.tasks_ok.append(task_id)
    
    def task_failed(self, task_id):
        """
            append a task id to failed tasks.
            >>> a=workunit()
            >>> a.task_failed('123')
            >>> a.tasks_fail
            deque(['123'])
        """
        self.tasks_fail.append(task_id)

    def new_task(self):
        """
            Create task object and append it to task list deque
            >>> a=workunit()
            >>> a.tasks #doctest: +ELLIPSIS
            deque([[0, <Assignment.task object at 0x...>]])
            >>> a.new_task()
            >>> a.tasks #doctest: +ELLIPSIS
            deque([[0, <Assignment.task object at 0x...>], [1, <Assignment.task object at 0x...>]])

        """
        description = False if not self.job else self.job.description
        self.tasks.append([len(self.tasks), task(self, self, Volunteer(), description )]) #TODO Store volunteer data somewhere.

    def status(self, expected=False):
        """
            workunit.status: Boolean property displaying if there're enought ok tasks.
            Unit testing:
            >>> workunit().status(0)
            True
            >>> workunit().status(1)
            False
        """
        if not expected:
            expected=self.expected
        return not len(self.tasks_ok) - expected

if __name__ == "__main__":
    """
        This should never be used as standalone but for unittests
    """
    import doctest
    doctest.testmod()
