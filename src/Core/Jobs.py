#!/usr/bin/env python
from Core.common import CommonFunctions
from WorkUnit import workunit
import logging

class job(CommonFunctions):
    def __init__(self, viewObject, pluginObject):
        """
            Returns a job object (workunits container)
            with plugin object and view object references.
        """
        self.viewObject = viewObject
        self.pluginObject = pluginObject

        self.read_config()
        self.initial_tasks = self.conf('main', 'initial_tasks')

        self.description = self.viewObject.description
        self.name = "Default job name"

        self.workunits = self.application.workunits

        logging.info('Creating job %s' , self)
        logging.info('\tProducing workunits... (%s) ', self.viewObject.workunits)
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

        for current_wk in range(0, number):
            logging.debug("Making working %s of %s", current_wk, number)
            a = workunit(self) # We create a new workunit, passing this object as a parent
            self.workunits.append(a) # Append it to our workunits queuqe
            if number is 1:
                return a
