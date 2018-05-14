# coding=utf-8

"""
Output the collected values to a ZeroMQ pub/ sub channel
"""

from diamond.handler.Handler import Handler

import random 
import time
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
        """try:
            self._bind()
        except Exception as e:
            print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS", e)"""

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
        #self.context = zmq.Context.instance()
        
        self.socket = self.context.socket(zmq.PUB)
        #self.socket = self.context.socket(zmq.PUSH)
        
        print("@@@@@@@@@@@@@@@@@@@@@@@@Zero MQ Port:", self.port)
        self.socket.bind("tcp://*:1234") # %s" % self.port)
        #self.socket.setsockopt(zmq.SUBSCRIBE, b"")
        
        #self.socket.bind("ipc:///tmp/zmqtest") 

        #time.sleep(1)

        print("2222222222222222222222222222222222222222222222")

        ctx = zmq.Context.instance()
        s = ctx.socket(zmq.REP)
        s.bind("tcp://*:1235")
        s.recv()
        s.send(b"GO")

        print("33333333333333333333333333333333333333333333333")

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
        print("@@@@@@@@@@@Le Jibe")
        if not zmq:
            return

        try:
            self._bind()
        except Exception as e:
            print("---------------->", e)

        """ctx = zmq.Context.instance()
        s = ctx.socket(zmq.REP)
        s.bind("tcp://*:1235")
        s.recv()
        s.send(b"GO")"""

        # Send data as ...
        # self.socket.send("%s" % str(metric))
        print("```````````````````````````Where is ZeroMQ ")
        #self.socket.send(b"Hello")
        #time.sleep(1)
        """for i in range(30):
            #time.sleep(2)
            topic = random.randrange(999, 10005)
            messagedata = numpy.random.rand(2, 2)
            
            #self.socket.send_pyobj(messagedata)
            
            #time.sleep(1)
            print("Ready to Send PyObject #", i, " = ... ", messagedata)
            

        #time.sleep(1) """

