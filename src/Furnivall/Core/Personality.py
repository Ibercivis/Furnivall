#!/usr/bin/env python

"""
    Previously personality objects, now I might need to merge
    it with userhandler

"""

import uuid
from Furnivall.Core.common import FurnivallPersistent

class User(FurnivallPersistent):
    def __init__(self, application):
        """

            user object
            TODO: Make this persistent

        """

        self.application = application
        self.permissions = ['None'] # TODO: make a system to grant a user permissions.
        # Woah, a user via a task might be able to create A WORKUNIT...
        self.workunits = {}
        self.jobs = {}
        self.tasks = {}
        self.password = ""
        self.initialized_views = {}

    def get_session_id(self):
        """

            Gets a *unique* session id.

        """
        if not self.id_:
            return uuid.uuid4().__str__()
        else:
            return self.id_

    def set_data(self, id_):
        """
           Returns user and host.
        """
        self.id_ = id_

    def set_password(self, password):
        self.password = password

    def grant_permission(self, permission):
        self.permissions.append(permission)

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

