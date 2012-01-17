#!/usr/bin/env python
"""
    Jobs
"""

from Core.common import FurnivallPersistent
from Core.WorkUnit import Workunit
import logging, uuid

class Job(FurnivallPersistent):
    """
        Job class
    """
    def __init__(self, view_object, plugin_object, request, id_, user):
        """
            Returns a job object (workunits container)
            with plugin object and view object references.
        """
        super(self.__class__, self).__init__()
        self.application = request.application
        self.id_ = id_
        self.view_object = view_object
        self.plugin_object = plugin_object
        self.user = user
        self.read_config()
        self.initial_tasks = self.conf('main', 'initial_tasks')

        self.description = self.view_object.description
        self.name = "Default job name"

        self.workunits = {}

        logging.info('Creating job %s' , self)
        logging.info('\tProducing workunits... (%s) ',
                self.view_object.workunits)

    def produce_initial_workunits(self):
        self.produce_workunits(self.view_object.workunits)

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
            logging.debug("Making workunit %s of %s", current_wk, number)
            # We create a new workunit, passing this object as a parent
            uuid_ = uuid.uuid4().__str__()
            logging.debug("We're going to create workunit %s" %(uuid_))
            try:
                work = Workunit(self.id_, self.user, uuid_, self.application)
                self.workunits[uuid_] = work # Append it to our workunits queuqe
                work.self_db = self.application.db['users'][self.user].jobs[self.id_].workunits[uuid_]
                work.do_initial_tasks()
                if number is 1:
                    return work
            except Exception, error:
                logging.info("Error: %s" %error)

