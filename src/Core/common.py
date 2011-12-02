#!/usr/bin/env python
"""
    Common functions.
"""

def get_highest_permission(self, permissions):
    """:
        Returns the higher permission between the given ones.
    """
    if "root" in permissions:
        return "root"
    if "researcher" in permissions:
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
