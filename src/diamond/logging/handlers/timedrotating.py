#coding=utf-8

from logging.handlers import TimedRotatingHandler as TRFH
import sys 

class TimedRotatingFileHandler(TRFH):
    def flush(self):
        try:
            super(TimedRotatingFileHandler, self).flush()
        except IOError:
            sys.stderr.write('TimedRotatingFileHandler received a IOError!')
            sys.stderr.flush()


