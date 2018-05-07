"""
The NetworkCollector class collects metrics on 
network interface usage using /proc/net/dev

### Dependencies

* /proc/net/dev

"""

import diamond.collector
from diamond.collector import str_to_bool 
import os
import re

try:
    import psutil
except ImportError:
    psutil = None

class NetworkCollector(diamond.collector.Collector):
    PROC = '/proc/net/dev'

    def get_default_config(self):
        """
        Returns the default collector settings
        """

        config = super(NetworkCollector, self).get_default_config()
        config.update({
            'path': 'network',
            'interfaces': ['eth', 'bond', 'em', 'plp', 'eno', 'enp', 
                'ens', 'enx'],
            'byte_unit': ['bit', 'byte'],
            'greedy': 'true',
        })

        return config

        # Initialize results
        results = {}

    def collect(self):
        """
        Collect network interface stats.
        """

        # Initialize results
        results = {}

        if os.access(self.PROC, os.R_OK):
            # Open file
            file = open( self.PROC )

            # Build Regular Expressions
            greed = ''
            if str_to_bool(self.config['greedy']):
                greed = '\S*'

            exp = (('^(?:\s*)((?:%s)%s):(?:\s*)' +
                '(?P<rx_bytes>\d+)(?:\s*)' + 
                '(?P<rx_packets>\w+)(?:\s*)'+ 
                '(?P<rx_errors>\d+)(?:\s*)'+ 
                '(?P<rx_drop>\d+)(?:\s*)'+ 
                '(?P<rx_fifo>\d+)(?:\s*)'+
                '(?P<rx_frame>\d+)(?:\s*)'+
                '(?P<rx_compressed>\d+)(?:\s*)'+
                '(?P<rx_multicast>\d+)(?:\s*)'+
                '(?P<tx_bytes>\d+)(?:\s*)'+
                '(?P<tx_packets>\w+)(?:\s*)'+ 
                '(?P<tx_errors>\d+)(?:\s*)'+ 
                '(?P<tx_drop>\d+)(?:\s*)'+ 
                '(?P<tx_fifo>\d+)(?:\s*)'+
                '(?P<tx_colls>\d+)(?:\s*)'+
                '(?P<tx_carrier>\d+)(?:\s*)'+
                '(?P<tx_compressed>\d+)(?:.*)$') %
                (('|'.join(self.config['interfaces'])), greed))
            
            reg = re.compile(exp)

            # Match Interfaces
            for line in file:
                match = reg.match(line)
                if match:
                    device = match.group(1)
                    results[device] = match.groupdict()

            # Close file
            file.close()


        for device in results:
            stats = results[device]

            for s, v in stats.items():
                # Get metric name 
                metric_name = '.'.join([device, s])
                # Get metric value
                metric_value = self.derivative(
                    metric_name, int(v), diamond.collector.MAX_COUNTER)

                # Convert rx_bytes and tx_bytes
                if s == 'rx_bytes' or s == 'tx_bytes':
                    convertor = diamond.convertor.binary(value=metric_value, unit='byte')

                    for u in self.config['byte_unit']:
                        # Public converted metric
                        self.publish( metric_name.replace('bytes', u),
                            convertor.get(unit=u), 2)
                    else:
                        # Publish Metric Derivative
                        self.publish(metric_name, metric_value)

        return None