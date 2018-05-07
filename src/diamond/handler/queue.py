# coding=utf-8

"""
This is a meta handler to act as a shim for the new threading model. 
Do not try to use it as a normal handler.
"""

from diamond.handler.Handler import Handler
import queue 

class QueueHandler(Handler):
    def __init__(self, config=None, queue=None, log=None):
        # Initialize Handler
        Handler.__init__(self, config=config, log=log)

        self.queue = queue

    def __del__(self):
        """
        Ensure as many of the metrics as possible are sent to handlers on a shutdown
        """
        self._flush()

    def _process(self, metric):
        """
        We skip any locking code due to the fact that this now a single process per collector
        
        Arguments:
            metric {[type]} -- [description]
        """
        try:
            print("Metric:", metric)
            # self.queue.put(metric, block=False)
            self.queue.put((1,1), False)
        except queue.Full:
            self.__throttle_error("Queue Full, check handlers for delays")

    def flush(self):
        return self._flush()

    def _flush(self):
        """
        We skip any locking code due to the fact that this is now a single process per collector
        """
        try:
            self.queue.put(None, block=False)
        except queue.Full:
            self._throttle_error("Queue Full, check handlers for delays")
    



