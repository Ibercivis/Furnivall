#!/usr/bin/env python

"""
    Assignment object and sons.
"""

import concurrent.futures, logging
#from sqlalchemy import Integuer, String
#from sqlalchemy.ext.declarative import declarative_base

# Assignment data {{{

class Assignment(object):
    """
        Assigment object
    """
    def __init__(self, workunit_id, user_id, application):
        """
            Superclass of task and Result.
            @param workunit_id: Id of the parent workunit of this assignment
            @type workunit_id: int
            @param user_id: Id of the user_ that got this assignment.
            @result: None.
        """
        self.application = application
        self.workunit = workunit_id
        self.user_ = user_id
        self.result = ""
        self.id_ = 0

    def append_to_workunit(self, place, notification):
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

        """

        getattr(self.workunit, place).append(notification)

    def globalize(self, id_, application):
        """
            Make this object part of the global queue, depending on the class
        """
        global_queue = getattr(application, self.__class__.__name__.lower())
        global_queue[id_] = self # TODO Check this.


# }}}

# Assignment {{{
class Task(Assignment):
    """
        Task object
    """

    def __init__(self, workunit_, user_, application):
        """
            @type workunit_: Core.Workunit object
            @param workunit_: Workunit directly responsible for this task.

            @type user: Personality.User object
            @param user: User directly responsible for this task

            @returns: Appends to workunit, in the workunit's tasks
                queue the result of launch_task from job's pluginobject.

            Asynchronously calls workunit's job pluginObject launch_task function.
            Set's up done_callback for task pointing to task.task_validator
            And appends this task to global tasks (as well as its id to parent ones)

            TODO: by default task's assigning a user_, empty, change it to FALSE.'

        """

        # Initialize superclass.
        super(Task, self).__init__(workunit_, user_, application)

        self.description = ""
        self.parent_job = getattr(self.workunit, "job")
        self.job_plugin = getattr(self.parent_job, 'pluginObject')
        # FIXME URGENTLY : This has to be a real task id ¿Passed by args?
        self.id_ = 0
        # We might have a async problem here.

        with concurrent.futures.ThreadPoolExecutor(max_workers = 20)\
                as executor: # Async call
            logging.debug('Creating executor for task: %s', self.id_)
            self.futureobject = executor.submit(self.launch)
            self.futureobject.add_done_callback(self.task_validator)
            self.globalize(self.application, self.id_)
            self.append_to_workunit('tasks', self.id_)

    def score_match(self, user_):
        """

            TODO: Should return a range between 0 and 10, but this is not yet defined.
            Tells how adequate this task is for this user_.
        """
        if user_ and self.description:
            return 1 # Dummy, do the real stuff.

    def launch(self):
        """
            Executes launch_task from workunit's job pluginObject.
            @returns: Assignment.Result object containing this task.

        """

        self.description = self.job_plugin.description

        logging.debug( "Task %s belongs to job %s and plugin %s, \
                executing task_executor for job's pluginobject",
                self.id_, self.parent_job, self.job_plugin.description)
        self.result = self.job_plugin.task_executor(self, self.workunit)

        return Result(self, self.description)

    def task_validator(self, result):
        #this is a bad name, because in BOINC validation is a wider concept
        """
            @type futureObject:
            @param futureObject: task

            Validates the task, calling the pluginObject's validate_task function.

            If task has passed, it'll append it to task_ok pool at it's creator,
            otherwise in tasks_fail

        """
        if getattr(self.workunit, 'job').pluginObject.validate_task(result):
            self.append_to_workunit('tasks_ok', self.id_)
            # TODO Fix this, it's not good on tasks_ok
        else:
            self.append_to_workunit('tasks_fail', self.id_)
            #quiza mejor self.creator.FailTask(self) ???
# }}}

# Result {{{
class Result(Assignment):
    """
        Result class. Creates a result object when a task is done
    """
    def __init__(self, task_, description):
        """
            @type task_
            @params task_
            @returns none
            Result object for a task.

        """

        super(Result, self).__init__(task_.workunit, task_.user_)
        self.description = description

    def consolidate_result(self):
        """
            Notify task's creator itself to result (this will be called when task is finished).
            Then, call creator's consolidate_result function (wich probably will call this tasks's plugin
            consolidate_result function)
        """

        # This adds to results deque in workunit this result object.
        self.append_to_workunit('results', self)

        self.result = ConsolidatedResult(self)
# }}}

# Consolidated result {{{
class ConsolidatedResult(Result):
    """
        Consolidated result.
    """
    def __init__(self, task_):
        """
           @param task_: Task to get result and creators
           @type task_: Assignment.task
           Consolidated Result, data property returns inittialized data.
        """
        super(ConsolidatedResult, self).__init__(task_.workunit, task_.user_)
        self.data = task_.job_plugin.consolidate_result(task_.result)
# }}}
