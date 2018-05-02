# coding=utf-8

from Handler import Handler

import socket
import time

class GraphiteHandler(Handler):
    """
    Implements the abstract Handler class, sending data to graphite.
    
    Arguments:
        Handler {[type]} -- [description]
    """
    def __init__(self, config=None):
        """
        Create a new instance of the GraphiteHandler class. 
        
        Keyword Arguments:
            config {[type]} -- [description] (default: {None})
        """
        Handler.__init__(self, config)

        # Initialize data
        self.socket = None
