#!/usr/bin/env python
import uuid

class Personality(object):
    """
        Personality object
    """
    def __init__(self, user, host, id_=False):
        """
            Base class for all personality module classes
            @param user: Username
            @type user: string
            @param host: host
            @type host: string
        """
        self.host = host
        self.user = user
        self.id_ = id_

class User(Personality):
    def __init__(self,  host=False, user=False):
        """
            user_ object.
            TODO: Make this persistent
        """
        super(User, self).__init__(user, host)

        self.workunits = {} # Woah, a user via a task might be able to create A WORKUNIT...
        self.jobs = {}
        self.tasks = {}

        self.initialized_views = {}
        self.session_id = self.get_session_id() # Not removing this,
        # might be needed in second phase (when re-implementing anonymous users)

    def get_session_id(self):
        """
            Gets a *unique* session id.
        """
        if not self.session_id:
            return uuid.uuid4()
        else:
            return self.session_id

    def set_data(self, host, user, id_):
        """
           Returns user and host.
        """
        self.host = host
        self.user = user

    @property
    def completed_tasks(self):
        """
            @returns: List of initialized task objects owned by this
                user that are finished
        """
        return [ task for task in self.tasks if self.application.tasks[task].done == True ]

    @property
    def all_tasks(self):
        """
            @returns: List of initialized task objects owned by this user
        """
        return [ self.application.tasks[task] for task in self.tasks ]

