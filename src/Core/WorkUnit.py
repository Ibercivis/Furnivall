#!/usr/bin/env python
from collections import deque
import logging
from Personality import User
from Assignment import ConsolidatedResult, task
from tornado.options import options, define

define('workunits_qeuque', default=deque())

class workunit(object):
    def __init__(self, job_id=0):
        """
            Simple job unit.
        """
        self.ConsolidatedResult = ""
        self.job = self.application.jobs[job_id]
        self.tasks = options.tasks
        self.tasks_ok = options.tasks_ok
        self.tasks_fail = options.tasks_failed

        self.expected = 0 #TODO this should get workunit expected tasks to return.
        self.results = options.results

        logging.info('\t\tWorkunit %s (%s tasks)', self, self.job.initial_tasks)

        for i in range(0, int(self.job.initial_tasks)):
            logging.info("Creating task number %s", i)
            self.new_task()

    def consolidate_result(self):
        """

            If workunit.status is true, it will create a *ConsolidatedResult* object,
            passing self.results and job's viewObject

            ConsolidatedResult will then store into it's data property a consolidated result
            got from self.job.viewObject.consolidate_result

        """

        if self.status:
            self.ConsolidatedResult = ConsolidatedResult(self.results,
                    self.job.pluginObject)
        # What about making this one assignment's child too and notify "job"
        # (creator) with notify_creator when it's got a consolidated result?

    def task_ok(self, task_id):
        """
            Append a task id to correct tasks queque.

            >>> a=workunit()
            >>> a.task_ok('123')
            >>> a.tasks_ok
            deque(['123'])
        """
        self.tasks_ok.append(task_id)

    def task_failed(self, task_id):
        """
            Append a task id to failed tasks queque

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
        self.tasks.append([len(self.tasks), Task(self, self, User(), description )]) #TODO User data should not be created here! Or should it? Tomorrow: CHeck this out

    @property
    def status(self, expected=False):
        """
            Workunit.status: Boolean property displaying if there're enought ok tasks.
            If called as property, expected can't be specified, will be got from self.expected.

            >>> workunit().status(0)
            True
            >>> workunit().status(1)
            False
        """
        if not expected:
            expected = self.expected
        return not len(self.tasks_ok) - expected

if __name__ == "__main__":
    # This should never be used as standalone but for unittests
    import doctest
    doctest.testmod()
