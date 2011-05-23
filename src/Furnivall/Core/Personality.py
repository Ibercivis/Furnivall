#!/usr/bin/env python
import collections
import tornado.session
"""
    Personality objects.
"""
class Personality(object):
    def __init__(self, user, host):
        self.host=host
        self.user=user

class Volunteer(Personality):
    def __init__(self,  host=False, user=False):
        # TODO Change the method volunteers work. Should be individual volunteers, by sessions, not by-task volunteers.
        """
            Volunteer object. Conttains host, user, current_tasks and completed_tasks for a user
            TODO: store everything about it in a datbase. Add auth to somewhere.
        """
        super(Volunteer, self).__init__(user, host)
        self.current_tasks=collections.deque()
        self.completed_tasks=collections.deque()

    def set_data(self, host, user, id_):
        self.host=host
        self.user=user
        self.id_=id_

class Researcher(Personality):
    def __init__(self, host, user):
        """
        """
        super(Researcher, self).__init__(user, host) 
        self.jobs=[]
