"""
    Furnivall core functions
"""

import logging
import tornado.web
from Core.UserHandler import ObjectManager
from Core.common import get_highest_permission, get_best_task

class Scheduler(ObjectManager):
    """
        Furnivall scheduler
    """

    def __init__(self, application, request, **kwargs):
        super(Scheduler, self).__init__(application, request, **kwargs)
        self.application.created_jobs = {}
        self.application.views = {}
        self.application.jobs = {}
        self.application.workunits = {}
        self.application.tasks = {}
        self.application.researchers = self.initialize_researchers()

    def assign_task(self, view=False, owner=False):
        """
            Assigns the best free task for a user to it.
            @param view: If provided, will get the tasks for that specific view
            @type view: string
            @param user: if provided, will only return tasks for a specific ownr
        """
        current_user = self.get_current_user()
        free_task = self.getfreetask(view=view, owner=owner)

        if free_task.user_.id_ == current_user.id_:
            logging.debug('[Debug] Sync error: user is already doing that task')
            return False

        logging.debug('[Debug] Creating user_ object. Giving it to a task')
        free_task.user_ = self.get_current_user()

    def getworkunit(self, job):
        """
            Gets a workunit (the first free one) from a job.
            If not job specified, returns all workunits
            @params job: Job to get workunit from.
            @type job: Job.job object
        """
        if not job:
            return self.application.workunits

        for work in job.workunits:
            logging.debug('Trying to return a free workunit.\
                    Currently processing %s', work)
            if not work.status: # TODO Check if work.status is well assigned
                logging.debug('%s is free!', work)
                return work

        logging.debug("No free workunits.\
                Creating new workunit object from %s", job)
        return job.produce_workunits()


    def getfreetask(self, view=False, owner=False):
        """
            Get a free task viable for the user, the one with more sCommonMatch
            @param view: If provided, will get the tasks for that specific view
            @type view: string
            @returns: Assignment.task object
        """
        for job in self.researcher_jobs(view, owner):
            logging.info("View from job %s is supported by user", job)
            return get_best_task(self.getworkunit(job))
        return

    def researcher_jobs(self, view=False, owner=False):
        """
            Get all jobs from all researchers in global queue
            @param view: If provided, will filter the jobs with this view
            @type view: string
            @returns: [ Jobs.job ]
            TODO Make it clear that view_objects have to define a __repr__ method
            that makes it able to check it against a string!!! (DOC)
            TODO: Re-check that jobs are in the [view.name, job_object] format!
        """

        if owner:
            for job in self.application.researchers[owner].jobs:
                if not view:
                    yield job
                else:
                    for view, job in job:
                        user = self.get_current_user()
                        if job.view_object.view == view and\
                                job.view_object.check_view(user):
                            yield job
        else:
            for researcher in self.application.researchers:
                for job in researcher.jobs:
                    for view, job in job:
                        user = self.get_current_user()
                        if view and not job.view_object.view == view:
                            continue
                        elif job.view_object.check_view(user):
                            yield job

    def initialize_researchers(self):
        """
            Initialize researchers, foreach researcher stored in database,
            recreate it
        """
        researchers = self.application.db.get("select * from auth where\
                permissions = 'reseacher' ")
        logging.debug("Researchers: %s", researchers)
        return researchers


class MainHandler(Scheduler):
    """
        MainHandler, inherits tornado's requesthandler and shows up display
        templastes
    """

    def login(self):
        """
            Checks out login against a database, given username and passwor
            as url params  and sets out a cookie.
        """
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")

        auth = self.application.db.get("select permissions from auth where\
                user='%s' and pass='%s'" %(username, password))
        db_user = self.application.db.get("select id as id_ from auth\
                where user='%s' and pass='%s'"  %(username, password))

        return ( db_user.id_, auth.permissions )

    def get(self, slug=False):
        """
            Tornado RequestHandler get function, renders slug as called
            from tornado, passing jobs and slug as argument.
            It also checks arguments to take actions when arguments are
            provided
        """

        auth = "None" # Default user permissions is None

        # Default to landing if /view/ called.
        # TODO: Do this as / too
        if not slug:
            logging.debug('[DEBUG] Defining slug as default')
            slug = "Landing"

        if "Login" in slug:
            user_id, auth = self.login()
            self.set_secure_cookie('username', user_id)

            # Get user after login (from cookie set in login process)
            user, auth = self.get_current_user()
            if not auth:
                auth = ""

            logging.debug('Logging in for user: %s', user)
            high_perm = get_highest_permission(auth)
            slug = self.application.special_login_slugs[high_perm]

        if slug is "Logout":
            self.clear_cookie('username')
            self.clear_cookie('permissions')
            slug = "Login"

        logging.debug('[Debug] Rendering template %s', slug)
        logging.debug('User has %s permissions', auth)

        self.render('%s' %(slug),
                user_permissions = auth,
                views = self.application.views,
                jobs = self.application.created_jobs,
                researchers = self.application.researchers,
                slug = slug )

        if self.get_argument('get_task', False):
            self.assign_task(view=self.get_argument('view'))
