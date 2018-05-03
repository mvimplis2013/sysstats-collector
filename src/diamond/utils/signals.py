# coding=utf-8

import signal

def signal_to_exception(signum, frame):
    """
    Called by the timeout alarm during the collector run time.
    
    Arguments:
        signum {[type]} -- [description]
        frame {[type]} -- [description]
    """
    if signum == signal.SIGALRM:
        raise SIGALRMException()
    if signum == signal.SIGHUP:
        raise SIGHUPException()
    if signum == signal.SIGUSR1:
        raise SIGUSR1Exception()
    if signum == signal.SIGUSR2:
        raise SIGUSR2Exception()
    raise SignalException(signum)


class SignalException(Exception):
    pass

class SIGALRMException(Exception):
    pass

class SIGHUPException(Exception):
    pass

class SIGUSR1Exception(Exception):
    pass

class SIGUSR2Exception(Exception):
    pass

    
