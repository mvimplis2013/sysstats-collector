# coding=utf-8

import logging 

import threading
from multiprocessing import Lock

import traceback
from configobj import ConfigObj 
import time

class Handler(object):
    """
    Handlers process metrics that are collected by Collectors
    """
    def __init__(self, config=None, log=None):
        """
        Create a new instance of the Handler class
        
        Keyword Arguments:
            config {[type]} -- [description] (default: {None})
            log {[type]} -- [description] (default: {None})
        """

        # Enabled ? Default to yes, but allow handlers to disable themselves
        self.enabled = True

        # Initialize log
        if log is None:
            self.log = logging.getLogger('diamond')
        else:
            self.log = log

        # Initialize blank configs
        self.config = ConfigObj()

        # Load default
        self.config.merge( self.get_default_config() )

        # Load in user config data
        self.config.merge( config )

        # Error logging throttling
        self.server_error_interval = float(
            self.config['server_error_interval'])
        self._errors = {}

        # Initialize Lock
        # self.lock = threading.Lock()
        self.lock = Lock()

    def get_default_config_help(self):
        """
        Returns the help text for the config options for this handler 
        """
        return {
            'get_default_config_help': 'get_default_config_help',
            'server_error_interval': ('How frequently to send repeated '
                'server errors'),
        }

    def get_default_config(self):
        """
        Return the default config for handler
        """
        return {
            'get_default_config': 'get_default_config',
            'server_error_interval': 120,
    }

    def _process(self, metric):
        """
        Decorator for processing handlers with a lock, catching exceptions
        
        Arguments:
            metric {[type]} -- [description]
        """
        if not self.enabled:
            return

        try:
            try:
                self.lock.acquire()
                self.process(metric)
            except Exception:
                self.log.error(traceback.format_exc())
        finally:
            if self.lock.locked():
                self.lock.release()

    def process(self, metric):
        """
        Process a Metric
        Should be overriden in subclasses
        
        Arguments:
            metric {[type]} -- [description]
        """
        raise NotImplementedError

    def _flush(self):
        """
        Decorator for flushing handlers with a lock, catching exceptions
        """
        if not self.enabled:
            return
        try:
            try:
                self.lock.acquire()
                self.flush()
            except Exception:
                self.log.error(traceback.format_exc())
        finally:
            if self.lock.locked():
                self.lock.release()

    def flush(self):
        """
        Flush Metrics

        Optional: Should be overridden in subclasses
        """
        pass

    def _throttle_error(self, msg, *args, **kwargs):
        """
        Avoids sending errors repeatedly. Waits at least 
        'self.server_error_interval' seconds before sending 
        the same error string to the error logging facility. 
        If not enough time has passed, it calls 'log.debug' instead        

        Receives the same parameters as 'Logger.error' and passes 
        them on to the selected logging function, but ignores all 
        parameters except the main message when checking the last 
        emission time.

        Arguments:
            msg {[type]} -- [description]

        :returns: the return value of `Logger.debug` or `Logger.error`
        """
        now = time.time()
        if msg in self._errors:
            if ((now - self._errors[msg]) >= self.server_error_interval):
                fn = self.log.error
                self.log.error
                self._errors[msg] = now
            else:
                fn = self.log.debug
        else:
            self._errors[msg] = now 
            fn = self.log.error

        return fn(msg, *args, **kwargs)

    def _reset_errors(self, msg=None):
        """
        Resets the logging throttle cache, so the next error 
        is emitted regardless of the value in `self.server_error_interval`
        
        :param msg: if present, only this key is reset. Otherwise, the 
            whole cache is cleaned.

        Keyword Arguments:
            msg {[type]} -- [description] (default: {None})
        """
        if msg is not None and msg in self._errors:
            del self._errors[msg]
        else:
            self._errors = {}




