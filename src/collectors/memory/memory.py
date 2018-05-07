"""
This class collects data on memory utilization.

Note that MemFree may report no memory free. This may not 
actually be the case, as memory is allocated to Buffers and 
Cache as well.

#### Dependencies

* /proc/meminfo
or "psutil"

"""
import diamond.collector

import os 
import logging

try:
    import psutil
except ImportError:
    psutil = None

_KEY_MAPPING = [
    'MemTotal',
    'MemFree',
    'MemAvailable',
    'Buffers',
    'Cached',
    'Active',
    'Dirty',
    'Inactive',
    'Shmem',
    'SwapTotal',
    'SwapFree',
    'SwapCached',
    'VmallocTotal',
    'VmallocUsed',
    'VmallocChunk',
    'Commited_AS',
]

class MemoryCollector(diamond.collector.Collector):
    PROC = '/proc/meminfo'

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
        self.log = logging.getLogger('zephyr')


    def get_default_config(self):
        """
        Returns the default collector settings
        """

    def collect(self):
        """
        Collect memory stats
        """
        if os.access(self.PROC, os.R_OK):
            file = open(self.PROC)
            data = file.read()
            file.close()

            memory_total = None
            memory_available = None

            for line in data.splitlines():
                try: 
                    name, value, units = line.split()
                    name = name.rstrip(':')
                    value = int(value)

                    if name not in _KEY_MAPPING:
                        continue 

                    if name in 'MemTotal':
                        memory_total = value
                    elif name in 'MemAvailable':
                        memory_available = value
                    
                except ValueError:
                    continue

            if memory_total is not None and memory_available is not None:
                memory_used = memory_total - memory_available
                memory_used_percent = memory_used / memory_total * 100.0

                print('Memory Used Percent: ', memory_used_percent)
                return True

                