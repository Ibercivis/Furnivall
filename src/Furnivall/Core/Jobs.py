#!/usr/bin/env python
from common import CommonFunctions
from WorkUnit import *
from Assignment import *
from collections import deque

class job(object, CommonFunctions):
    def __init__(self):
        self.read_config
        self.initial_tasks=self.conf('main', 'initial_tasks')
        self.workunits=deque()
    
    def produce_workunit(self):
        """
            >>> a=workunit()
            >>> print a # doctest: +ELLIPSIS
            <WorkUnit.workunit object at 0x...>
            >>> print a.tasks # doctest: +ELLIPSIS
            deque([[0, <Assignment.task object at 0x...>]])
        """
        wk=workunit(self)
        self.workunits.append(wk)
        return wk

if __name__ == "__main__":
    """
        This should never be used as standalone but for unittests
    """
    import doctest
    doctest.testmod()
