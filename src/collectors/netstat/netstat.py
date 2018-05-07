"""
The NetstatCollector class collects metrics on number 
of connections in each state.

#### Dependencies

* /proc/net/tcp

"""

import diamond.collector

class NetstatCollector(diamond.collector.Collector):
    PROC_TCP = "/proc/net/tcp"

    STATE = {
        '01': 'ESTABLISHED',
        '02': 'SYN_SENT',
        '03': 'SYN_RECV',
        '04': 'FIN_WAIT1',
        '05': 'FIN_WAIT2',
        '06': 'TIME_WAIT',
        '07': 'CLOSE',
        '08': 'CLOSE_WAIT', 
        '09': 'LAST_ACK',
        '0A': 'LISTEN',
        '0B': 'CLOSING'
    }

    def collect(self):
        """
        Overrides the Collector.collect() method
        """

        content = self._load()

        result = dict((self.STATE[num], 0) for num in self.STATE)
        
        for line in content:
            line_array = self._remove_empty(line.split(' '))
            print('Line Array:', line_array)
            state = self.STATE[line_array[3]]

            result[state] += 1

        for state in result:
            print('* ', state, result[state])

    @staticmethod 
    def _load():
        """ Read the table of tcp connections & remove header """
        with open(NetstatCollector.PROC_TCP, 'r') as f:
            content = f.readlines()
            content.pop(0);
        
        return content

    @staticmethod
    def _remove_empty(array):
        return [x for x in array if x != '']
