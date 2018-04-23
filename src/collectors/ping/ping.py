"""
Collect icmp round trip times.
Only valid for ipv4 hosts currently.

### Dependencies

* ping 

"""

class PingCollector():
    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(PingCollector, self).get_default_config()
        config.update({
            'path': 'ping',
            'bin': '/bin/ping'
        })

        retirn config

    def collect(self):
        for key in self.config.keys():
            if key[:7] == "target_":
                host = self.config[key]
