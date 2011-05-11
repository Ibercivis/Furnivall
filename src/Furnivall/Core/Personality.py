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
        super(Volunteer, self).__init__()
        self.current_tasks=deque()
        self.completed_tasks=deque()

class Researcher(Personality):
    def __init__(self, host, user):
        super(Researcher, self).__init__() 
        self.jobs=[]
