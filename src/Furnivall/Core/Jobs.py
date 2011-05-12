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
        self.read_config
        self.initial_tasks=self.conf('main', 'initial_tasks')
        self.workunits=deque()
        self.viewObject=viewObject
        self.pluginObject=getattr(viewObject.pluginmodule, viewObject.pluginclass)()
        # TODO: Produce the workunits. Where should I decide the number of workunits?
        # Each job contains a view object, so I suppose we should do it there.
        # By user interaction????
        # asdf asdf asdf asdf ???
    
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
