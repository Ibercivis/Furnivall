#!/usr/bin/env python
from common import CommonFunctions
from WorkUnit import *
from Assignment import *
from collections import deque
from Core.common import log

class job(object, CommonFunctions):
    def __init__(self, viewObject, pluginObject):
        """
            Returns a job object (workunits container)
            with plugin object and view object references.
        """
        self.read_config()
        self.description=viewObject.description
        self.initial_tasks=self.conf('main', 'initial_tasks')
        self.workunits=deque()
        self.name="Default job name"
        self.viewObject=viewObject
        self.pluginObject=pluginObject

        log('Creating job %s' %(self))
        log('\tProducing workunits... (%s) ' %self.viewObject.workunits)
        self.produce_workunits(self.viewObject.workunits)
    
    def produce_workunits(self, number=1):
        """
            Creates N new workunit objects, with this job as job and
            appends them to our workunits queque.
            If N is 1, it will also return the created workunit.

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

        for n in range(0, number): 
            a=workunit(self) # We 
            self.workunits.append(a) # Append it to our workunits queuqe
            if number is 1: return a #

if __name__ == "__main__":
    """
        This should never be used as standalone but for unittests
    """
    import doctest
    from Tests import viewtest
    import Tests
    doctest.testmod()
