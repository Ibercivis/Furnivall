#!/usr/bin/env python
from common import CommonFunctions
from WorkUnit import *
from Assignment import *
from collections import deque

class job(object, CommonFunctions):
    def __init__(self, viewObject):
        """
            Returns a job object (workunits container)
            with plugin object and view object references.
        """
        self.read_config()
        self.description=viewObject.description
        self.initial_tasks=self.conf('main', 'initial_tasks')
        self.workunits=deque()
        self.viewObject=viewObject
        self.pluginObject=getattr(viewObject.pluginmodule, viewObject.pluginclass)()
        self.produce_workunits(self.viewObject.workunits) # TODO Keep track of workunits, and create new ones, and so on.
    
    def produce_workunits(self, number=1):
        """
            >>> a=job(viewtest())
            >>> len(a.workunits)
            10
            >>> a.produce_workunits(10)
            >>> len(a.workunits)
            20
            >>> print a.workunits[0] # doctest: +ELLIPSIS
            <WorkUnit.workunit object at 0x...>
            >>> print a.workunits[0].tasks # doctest: +ELLIPSIS
            deque([[0, <Assignment.task object at 0x...>]])
        """
        for n in range(0, number): self.workunits.append(workunit(self))

if __name__ == "__main__":
    """
        This should never be used as standalone but for unittests
    """
    import doctest
    from Tests import viewtest
    import Tests
    doctest.testmod()
