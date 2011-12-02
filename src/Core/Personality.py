#!/usr/bin/env python

"""
    Previously personality objects, now I might need to merge
    it with userhandler

"""

import uuid

class User(object):
    """
        User Object
    """
    def __init__(self, application, user_object=False, id_=False):
        """
            user_ object.
            TODO: Make this persistent
        """

        self.application = application
        self.user = user_object
        self.id_ = id_

        # Woah, a user via a task might be able to create A WORKUNIT...
        self.workunits = {}
        self.jobs = {}
        self.tasks = {}
        self.initialized_views = {}

    def get_session_id(self):
        """
            Gets a *unique* session id.
        """
        if not self.id_:
            return uuid.uuid4()
        else:
            return self.id_

    def set_data(self, user, id_):
        """
           Returns user and host.
        """
        self.id_ = id_
        self.user = user

    @property
    def completed_tasks(self):
        """
            @returns: List of initialized task objects owned by this
                user that are finished
        """
        return [ task for task in self.tasks\
                if self.application.tasks[task].done == True ]

    @property
    def all_tasks(self):
        """
            @returns: List of initialized task objects owned by this user
        """
        return [ self.application.tasks[task] for task in self.tasks ]

