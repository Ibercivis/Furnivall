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
        try:
            self.application.researchers = self.application.db['researchers']
        except KeyError, err:
            self.application.db['researchers']=[]
            self.application.researchers = self.application.db['researchers']
            logging.debug("Could not get researchers, they are not yet\
                    created: %s", err)

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
        return free_task.id_

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

class LoginHandler(tornado.web.RequestHandler):
    def get(self, slug="auth"):
        if slug == "auth":
            user_id = self.get_secure_cookie('username', False)
            if not user_id:
                self.set_secure_cookie('username', user.id_)
            auth = user.permissions
            high_perm = get_highest_permission(auth)
            slug = self.application.special_login_slugs[high_perm]

        if slug == "out":
            self.clear_cookie('username')
            self.clear_cookie('auth')
            slug = "Login"



    def login(self):
        """
            Checks out login against a database, given username and passwor
            as url params  and sets out a cookie.
        """
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        try:
            user = self.application.db['users'][username]
            if user.password == password:
                return username
            else:
                return False
        except KeyError:
            return False

class MainHandler(Scheduler):
    """
        MainHandler, inherits tornado's requesthandler and shows up display
        templastes
    """


    def get(self, slug="Landing"):
        """
            Tornado RequestHandler get function, renders slug as called
            from tornado, passing jobs and slug as argument.
            It also checks arguments to take actions when arguments are
            provided
        """
        user = False
        auth = [ "None" ]

        try:
            user_id = self.get_secure_cookie('username', 0) # If noone tryed to auth user anon user
            if not user_id:
                user_id = 0
            try:
                user = self.application.db['users'][user_id]

            except KeyError, error:
                logging.debug("Bad user id. User might be trying something strange %s %s " %(user_id, user))

        except Exception, err:
            logging.info(err)

        if user_id != 0 and not user: # TODO Insert anon user as first user in db. Pass will be empty.
            self.redirect('/Login')

        logging.debug('[Debug] Rendering template %s', slug)

        self.render('%s' %(slug),
                user_permissions = auth,
                views = self.application.views,
                jobs = self.application.created_jobs,
                researchers = self.application.researchers,
                slug = slug )

        if self.get_argument('get_task', False):
            task = self.assign_task(view=self.get_argument('view'))
            self.render_task(task)
