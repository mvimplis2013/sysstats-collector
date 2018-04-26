# coding=utf-8

"""
The Collector class is a base class for all metric collectors.
"""

import os 
import socket
import platform
import logging
import configobj
import time
import re
import subprocess

from diamond.metric import Metric
from diamond.utils.config import load_config
from error import DiamondException

class Collector():
    """
    The Collector class is a base class for all metric collectors.
    """

    def __init__(self, config=None, handlers=[], name=None, configfile=None):
        """
        Create a new instance of the Collector class
        
        Keyword Arguments:
            config {[type]} -- [description] (default: {None})
            handlers {list} -- [description] (default: {[]})
            name {[type]} -- [description] (default: {None})
            configfile {[type]} -- [description] (default: {None})
        """

        # Initialize Logger
        self.log = logging.getLogger('diamond')
        self.log.setLevel(logging.DEBUG)

        # Create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Add handlers to logger
        self.log.addHandler(ch)

    def collect(self):
        """
        Default collector method
        """

        # raise NotImplementedError()

    def _run(self):
        """
        Run the collector unless it's already running
        """

        try:
            start_time = time.time()
            
            # Collect Data
            self.collect()

            end_time = time.time()
            collector_time = int((end_time - start_time) * 1000)

            self.log.debug('Collection took %s ms', collector_time)
        finally:
            print('')

class ProcessCollector(Collector):
    """
    Collector with helpers for handling running commands with/ without sudo 
    
    Arguments:
        Collector {[type]} -- [description]
    """

    def run_command(self, args):
        if 'bin' not in self.config:
            raise Exception('config does not have any binary configured')
        if not os.access(self.config['bin'], os.X_OK):
            raise Exception('%s is not executable' % self.config['bin'])
        
        try: 
            command = args
            command.insert(0, self.config['bin'])

            if str_to_bool(self.config['use_sudo']):
                command.insert(0, self.config['sudo_cmd'])

            return subprocess.Popen(command, stdout=subprocess.PIPE).communicate()
        except OSError:
            self.log.exception("Unable to run %s", command)
            return None





