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

class Researcher(Personality, Core.common.CommonFunctions):
    def __init__(self,  host=False, user=False):
        """
            Researcher object.
            *TODO: store everything about it in a datbase. Add auth to somewhere.*
        """
        super(self.__class__, self).__init__(user, host)
        self.read_config()
        self.current_tasks=collections.deque()
        self.completed_tasks=collections.deque()
        self.initialize_views={}
        self.jobs=[]


    def set_data(self, host, user, id_):
        """
            Returns host user and id from a researcher object.
        """
        self.host=host
        self.user=user
        self.id_=id_

class Volunteer(Personality):
    def __init__(self,  host=False, user=False):
        """

            Volunteer object.
            TODO Change the method volunteers work. Should be individual volunteers, by sessions, not by-task volunteers. (ongoing)

        """
        super(Volunteer, self).__init__(user, host)
        self.current_tasks=collections.deque()
        self.completed_tasks=collections.deque()
        self.session_id=self.get_session_id()

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
