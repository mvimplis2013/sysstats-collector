# coding=utf-8

"""
Output the collected values to a ZeroMQ pub/ sub channel
"""

from diamond.handler.Handler import Handler

import random 
import numpy

try:
    import zmq
except ImportError:
    zmq = None

class zmqHandler(Handler):
    """
    Implements the abstract Handler class.
    Sending data to a ZeroMQ pub channel
    
    Arguments:
        Handler {[type]} -- [description]
    """

    def __init__(self, config=None):
        """
        Create a new instance of zmqHandler class
        
        Keyword Arguments:
            config {[type]} -- [description] (default: {None})
        """

        # Initialize Handler
        Handler.__init__(self, config)

        if not zmq:
            self.log.error("zmq import failed. Handler disabled")
            self.enabled = False
            return

        # Initialize data 
        self.context = None
        
        self.socket = None

        # Initialize options
        self.port = int(self.config['port'])

        # Create ZMQ pub socket and bind
        self._bind()

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for the handler
        """
        config = super(zmqHandler, self).get_default_config_help()

        config.update({
            'port': '',
        })

        return config

    def get_default_config(self):
        """
        Returns the default config for the handler
        """
        config = super(zmqHandler, self).get_default_config()

        config.update({
            'port': 1234,
        })

        return config

    def _bind(self):
        """
        Create PUB socket and bind
        """
        if not zmq:
            return
        
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        print("@@@@@@@@@@@@@@@@@@@@@@@@Zero MQ Port:", self.port)
        self.socket.bind("tcp://127.0.0.1:5556") # % self.port)

    def __del__(self):
        """
        Destroy instance of the zmqHandler class
        """
        pass

    def process(self, metric):
        """
        Process a metric and send it to zmq pub socket
        
        Arguments:
            metric {[type]} -- [description]
        """
        print('**************************** Navigating the Labyrinth ********************************************')

        if not zmq:
            self.log.info("ZMQ not available")
            return

        # Send data as ...
        # self.socket.send("%s" % str(metric))
        print("```````````````````````````Where is ZeroMQ ")
        #self.socket.send_string("%s" % "Hello")
        topic = random.randrange(999, 10005)
        messagedata = numpy.random.rand(2,2)

        try:
            #self.socket.send_string("%i %i" % (topic, messagedata))
            self.socket.send_pyobj(messagedata)
        except Exception as e:
            print(e)

