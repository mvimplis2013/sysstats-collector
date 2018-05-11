# coding=utf-8

"""
Uses /proc to collect available system entropy

#### Dependencies
# 
# /proc/sys/kernel/random/entropy_avail
# 
"""

import diamond.collector
import os

class EntropyStatCollector(diamond.collector.Collector):
    PROC = '/proc/sys/kernel/random/entropy_avail'

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(EntropyStatCollector, self).get_default_config()

        config.update({
            'path': 'entropy'
        })

        return config

    def collect(self):
        if not os.access(self.PROC, os.R_OK):
            return None

        # File Open
        entropy_file = open(self.PROC)

        # Read Value
        entropy = entropy_file.read().strip()

        # Close File
        entropy_file.close()

        # Publish Value
        self.publish_gauge("available", entropy)

