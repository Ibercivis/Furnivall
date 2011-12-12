#!/usr/bin/env python
"""
    Workunit
"""
from collections import deque
import logging
from Core.Personality import User
from Core.Assignment import ConsolidatedResult, Task
from tornado.options import options, define

define('workunits_qeuque', default=deque())

class Workunit(object):
    """
        Workunit
    """
    def __init__(self, job_id=0, application=False):
        """
            Simple job unit.
        """
        self.consolidatedres = ""
        self.application = application
        if application:
            self.job = self.application.jobs[job_id]
        else:
            raise(Exception('Failure getting application, this wk is lost'))
        self.task = {}
        self.result = {}

        #TODO this should get workunit expected tasks to return.
        self.expected = 0
        self.results = options.results

        logging.info('\t\tWorkunit %s (%s tasks)', self, self.job.initial_tasks)

        for i in range(0, int(self.job.initial_tasks)):
            logging.info("Creating task number %s", i)
            self.new_task()

    def consolidate_result(self):
        """

            If workunit.status is true, it will create a *consolidatedres* object,
            passing self.results and job's view_object

            consolidatedres will then store into it's data property a consolidated result
            got from self.job.view_object.consolidate_result

        """

        if self.status:
            self.consolidatedres = ConsolidatedResult(self.results,
                    self.job.plugin_object)
        # What about making this one assignment's child too and notify "job"
        # (creator) with notify_creator when it's got a consolidated result?

    def new_task(self):
        """
            Create task object and append it to task list deque
            User is empty at this point, it has to be assigned later.
            On task creation it globalizes itself, adding the task
            object to global tasks queue. Then returns the ID for it to
            be appended to local tasks queue.
            TODO: Check user assignation
        """
        id_ = Task(self, False, self.application ).id_
        self.tasks.append(id_)

    @property
    def status(self, expected=False):
        """
            Workunit.status: Boolean property displaying if there're enought ok tasks.
            If called as property, expected can't be specified, will be got from self.expected.
        """
        if not expected:
            expected = self.expected
        return not len(self.tasks_ok) - expected

    @property
    def tasks_ok(self):
        """
            Check all the tasks for this workunit with status true.
            Wich means they're finished and possitive in validation.
        """
        return [ task for task in self.tasks\
                if self.application.tasks[task].status == True ]

if __name__ == "__main__":
    # This should never be used as standalone but for unittests
    import doctest
    doctest.testmod()
