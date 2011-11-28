#!/usr/bin/env python
import collections
#import tornado.session
import uuid
import Core.common
"""
    Personality objects.
"""
class Personality(object):
    def __init__(self, user, host, id_=False):
        """

            Inherited by all personality-based objects

        """
        self.host=host
        self.user=user
        self.id_=id_

class User(Personality):
    def __init__(self,  host=False, user=False):
        """

            user_ object.
            TODO: Make this persistent
        """
        super(User, self).__init__(user, host)
        self.current_tasks=collections.deque()
        self.completed_tasks=collections.deque()
        self.initialized_views={}
        self.jobs=collections.deque()
        self.session_id=self.get_session_id() # Not removing this,
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
        self.host=host
        self.user=user
