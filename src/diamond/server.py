# coding=utf-8

import logging
import multiprocessing
import os
import signal
import sys
import time

try:
    from setproctitle import getproctitle, setproctitle
except ImportError:
    setrpoctitle = None

# Path Fix
sys.path.append(
    os.path.abspath(
        os.path.join( 
            os.path.dirname(__file__), "../"
        )
    )       
)

    def str_to_bool(value):
        """
        Converts string truthy/ falsey string to a bool.
        Empty strings are false. 
        
        Arguments:
            value {[type]} -- [description]
        """
        if isinstance(value, basestring):
            value = value.strip().lower()

            if value in ['true', 't', 'yes', 'y']:
                return True
            elif value in ['false', 'f', 'no']:
                return False
            else:
                raise NotImplementedError("Unknown bool %s" % value)

            return value    

class Server():
    """
    Server class loads and starts Handlers and Collectors
    """

    def __init__(self, configfile):
        # Initialize Logging
        self.log = logging.getLogger('diamond')

        # Initialize Members
        self.configfile = configfile
        self.config = None
        self.handlers = []
        self.handler_queue = []
        self.modules = {}
        self.metric_queue = None

        # We do this weird process title swap around to 
        # get the sync manager correct for ps
        if setproctitle:
            oldproctitle = getproctitle()
            setproctitle('%s - SyncManger' % getproctitle())
        
        self.manager = multiprocessing.Manager()

        if setproctitle:
            setproctitle(oldproctitle)

    def run(self):
        """
        Load handler and collector classes and 
        then start collectors 
        """

        ##################################################
        # Config
        ##################################################
        self.config = load_config(self.configfile)

        collectors = load_collectors(self.config['server']['collectors_path'])
        metric_queue_size = int(self.config['server'].get('metric_queue_size', 16384))

        self.metric_queue = self.manager.Queue(maxsize=metric_queue_size)
        self.log.debug('metric_queue_size: %d', metric_queue_size)

        ###################################################
        # Handlers
        #
        # TODO: Eventually move each handler to it's own 
        #       process space
        ###################################################
        if 'handlers_path' in self.config['server']:
            handlers_path = self.config['server']['handlers_path']

            # Make a list 
            if isinstance(value, basestring):
                handlers_path = handlers_path.split(',')
                handlers_path = map(str.strip, handlers_path)
                self.config['server']['hadlers_path'] = handlers_path

            load_include_path(handlers_path)
        
        if 'handlers' not in self.config['server']:
            self.log.critical('handlers missing from server section in config')
            sys.exit(1)

        handlers = self.config['server'].get('handlers')
        if isinstance(handlers, basestring):
            handlers = [handlers]

        # Prevent the Queue handler from being a normal handler
        if 'diamond.handler.queue.QueueHandler' in handlers:
            handlers.remove('diamond.handlers.queue.QueueHandler')

        self.handlers = load_handlers(self.conig, handlers)

        QueueHandler = load_dynamic_class(
            'diamond.handler.queue.QueueHandler',
            Handler
        )

        self.handler_queue = QueueHandler(
            config=self.config, queue = self.metric_queue, 
                log=self.log)

        handlers_process = multiprocessing.Process(
            name = "Handlers",
            target = handler_process,
            args = (self.handlers, self.metric_queue, self.log),
        )

        handlers_process.daemon = True
        handlers_process.start()

        ##############################################
        # Signals
        ##############################################
        if hasattr(signal, 'SIGHUP'):
            signal.signal(signal.SIGHUP, signal_to_exception)

        ##############################################

        while True:
            try:
                active_children = multiprocessing.active_children()
                running_process = []
                for process in active_children:
                    running_processes.append(process.name)
                running_processes = set(running_processes)

                ############################################
                # Collectors 
                ############################################
                running_collectors = []
                for collector, config in self.config['collectors'].iteritems():
                    if config.get('enabled', False) is not True:
                        continue
                    running_collectors.append(collector)
                running_collectors = set(running_collectors)
