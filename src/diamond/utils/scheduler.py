# coding=utf-8

import time
import math
import multiprocessing
import os
import random
import sys
import signal

try:
    from setproctitle import setproctitle, getproctitle
except ImportError:
    setproctitle = None

def collector_process(collector, metric_queue, log):
    