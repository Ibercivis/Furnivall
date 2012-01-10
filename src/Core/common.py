#!/usr/bin/env python
"""
    Common functions.
"""

def get_best_task(self, work=False):

    """
        @param work: Workunit
        @type work: WorkUnit.workunit
        @returns: Assignment.task object
        Get the best task ordered by ScommonMatch if it has not a user_ assigned
        If no task available to return,
        # TODO: change ScommonMatch in workunit to call the plugin/view's
        # compatibility class. TODO: Make a view's compatibility class
     """

    try:
        return [sorted(task, key = lambda t: t.score_match()) \
            for task in work.tasks\
            if not task.user_.session_id ][0]
    except IndexError, exception:
        logging.debug("Exception %s at get_best_task", exception)
        return work.new_task

def get_highest_permission(perm):
    """:
        Returns the higher permission between the given ones.
    """
    import logging
    logging.debug("Getting higher permission from %s", perm)
    if "root" in perm:
        return "root"
    if "researcher" in perm:
        return "researcher"
    else:
        return "user"

class commonClass(object):
    """
        Common functions for all furnivall
        Right now, only config management is defined here.
    """
    def __init__(self):
        self.config = ""

    def read_config(self):
        """
            Reads default furnivall config from ./furnivall.conf ~/.furnivall.conf and /etc/furnivall.ConfigPars
            Stores it in self.conf and returns it.
        """
        import ConfigParser, os
        config = ConfigParser.ConfigParser()
        config.read(['furnivall.conf', os.path.expanduser('~/.furnivall.conf'), '/etc/furnivall.conf'])
        self.config = config
        return config # Optional if you use CF.conf().

    def conf(self, section, option):
        """
            Custom function to read conf in two steps instead of three (..).
        """
        return self.config.get(section, option)
