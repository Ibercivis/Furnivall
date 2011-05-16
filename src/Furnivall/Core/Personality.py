#!/usr/bin/env python
import collections
"""
    Personality objects.
"""
class Personality(object):
    def __init__(self, user, host):
        self.host=host
        self.user=user

class Volunteer(Personality):
    def __init__(self,  host=False, user=False):
        """
            Volunteer object. Conttains host, user, current_tasks and completed_tasks for a user
            TODO: store everything about it in a datbase. Add auth to somewhere.
        """
        super(Volunteer, self).__init__(user, host)
        self.current_tasks=collections.deque()
        self.completed_tasks=collections.deque()

class Researcher(Personality):
    def __init__(self, host, user):
        """
        """
        super(Researcher, self).__init__(user, host) 
        self.jobs=[]
