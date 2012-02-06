#!/usr/bin/env python
"""
    Workunit
"""
from Furnivall.Core.common import FurnivallPersistent
from Furnivall.Core.Personality import User
from Furnivall.Core.Assignment import ConsolidatedResult, Task
import logging, concurrent.futures

class Workunit(FurnivallPersistent):
    """
        Workunit
    """
    def __init__(self, job_id, user, workunit, application = False):
        """
            Simple job unit.
        """

        try:
            self.self_db = application.db['users'][user].jobs[job_id].workunits[workunit]
        except:
            application.db['users'][user].jobs[job_id].workunits[workunit] = ""
            self.self_db = application.db['users'][user].jobs[job_id].workunits[workunit]

        self.consolidatedres = ""
        self.application = application
        self.user = user

        if application:
            self.job = self.application.db['users'][user].jobs[job_id]
        else:
            raise(Exception('Failure getting application, this wk is lost'))

        self.tasks = {}
        self.result = {}

        #TODO this should get workunit expected tasks to return.
        self.expected = 0
        self.results = {}

    def do_initial_tasks(self):
        """
            Create job.initial_tasks tasks
        """
        self.create_tasks(self.job.initial_tasks, self.user)

    def create_tasks(self, number, user):
        """
            Creates a number of tasks objects and launches them on different threads.
        """
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=int(number))
        tasks = [Task(self, self.user, self.application) for _ in range(int(number)) ]
        for task, future in [(i, executor.submit(i)) for i in tasks]:
            try:
                future.add_done_callback(task.task_validator)
            except concurrent.futures.TimeoutError:
                print("this took too long...")
                task.interrupt()

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

    @property
    def status(self, expected=False):
        """
            Workunit.status: Boolean property displaying if there're enought ok tasks.
            If called as property, expected can't be specified, will be got from self.expected.
        """
        if not expected:
            expected = self.expected
        return len(self.tasks_ok) >= expected

    @property
    def tasks_free(self):
        return [self.self_db.tasks[uuid] for uuid in self.self_db.tasks if self.self_db.tasks[uuid].status == -1 ]
    

    @property
    def tasks_running(self):
        """
            Returns the number of tasks that are currently running  for this workunit
        """
        return [self.self_db.tasks[uuid] for uuid in self.self_db.tasks if self.self_db.tasks[uuid].status == -2 ]

    @property
    def tasks_failed(self):
        """
            Returns the number of tasks that have failed for this workunit
        """
        return [self.self_db.tasks[uuid] for uuid in self.self_db.tasks if self.self_db.tasks[uuid].status == False ]

    @property
    def tasks_ok(self):
        """
            Check all the tasks for this workunit with status true.
            Wich means they're finished and possitive in validation.
        """
        return [self.self_db.tasks[uuid] for uuid in self.self_db.tasks if self.self_db.tasks[uuid].status == True ]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
