#!/usr/bin/env python
"""
    Personality objects.
"""
class Personality(object):
    def __init__(self, name):
        self.host=host
        self.user=user

class Volunteer(Personality):
    def __init__(self,  host=False, user=False):
        """
            Volunteer object. Conttains host, user, current_tasks and completed_tasks for a user
            TODO: store everything about it in a datbase. Add auth to somewhere.
        """
        super(Volunteer, self).__init__()
        self.current_tasks=deque()
        self.completed_tasks=deque()

class Researcher(Personality):
    def __init__(self, host, user):
        """
        """
        super(Researcher, self).__init__() 
        self.jobs=[]
