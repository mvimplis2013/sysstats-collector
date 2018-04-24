"""
Collect icmp round trip times.
Only valid for ipv4 hosts currently.

### Dependencies

* ping 

### Configuration

Configuration is done by:

Create a file named: PingCollector.conf in the collectors_config_path

* enabled = true
* interval = 60
* target_1 = example.org
* target_fw = 102.168.0.1
* target_localhost = localhost

Test your configuration using the following command:

diamond-setup --print -C PingCollector

You should get a response back that indicates ... 'enabled': True

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
                metric_name = host.replace('.', '_')

                ping = self.run_command(['-nq', '-c 1', host])
