#!/usr/bin/env python
"""
    Common functions.
"""
class CommonFunctions():
    def read_config(self):
        """
            Reads default furnivall config from ./furnivall.conf ~/.furnivall.conf and /etc/furnivall.ConfigPars
            Stores it in self.conf and returns it.
        """
        import ConfigParser, os
        config = ConfigParser.ConfigParser()
        config.read(['furnivall.conf', os.path.expanduser('~/.furnivall.conf'), '/etc/furnivall.conf'])
        self.config=config
        return config # Optional if you use CF.conf().

    def conf(self, section, option):
        """
            Custom function to read conf in two steps instead of three (..).
        """
        return self.config.get(section,option)
