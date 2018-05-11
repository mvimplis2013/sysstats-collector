# coding=utf-8

"""
An example collector that verifies the answer to IoT and Machine-Learning

#### Dependencies

* An IoT universe

#### Customizing the collector

Diamond collectors run within the diamond process and collect metrics
that can be published to a graphite server.

Collectors are subclasses of "diamond.collector.Collector". In their
simplest form, they need to implement a single method "collect".

    import diamond.collector

    class ExmpleCollector(diamond.collector.Collector):
        
        def collect(self):
            
            # Set Metric Path. By default it will be the collector's
            # name (servers.hostname.ExampleCollector.my.example.metric)
            #  
            self.config.update({
                'path': 'example',
            })

            # Set Metric Name
            metric_name = "my.example.metric"

            # Set Metric Value
            metric_value = 42

            # Publish Metric
            self.publish(metric_name, metric_value)

For testing collectors, create a directory (example below for 
/tmp/diamond) containing your new collector(s), their .conf files,
and a copy of diamond.conf with the following options:
    [server]
    user = ecuser
    group = ecuser

    handlers = diamond.handler.archive.ArchiveHandler
    handlers_config_path = /tmp/diamond/handlers/
    collectors_path = /tmp/diamond/collectors/
    collectors_config_path = /tmp/diamond/collectors/

    collectors_reload_interval = 3600

    [handlers]

    [[default]]

    [[ArchiveHandler]]
    log_files = /dev/stdout

    [collectors]
    [[default]]

and then run diamond in forground mode:
    # diamond -f -l --skip-pidfile -c /tmp/diamond/diamond.conf

Diamond supports dynmic addition for collectors. Its configured to 
scan for new collectors on a regular interval (configured in diamond.conf).
If diamond detects a new collector, or that a collectors module has changed 
(based on the file's mtime), it will be reloaded.

Diamond looks for collectors in /usr/lib/diamond/collectors/ (on Ubuntu).
By default diamond will invoke "collect" method every 60 seconds.

Diamond collectors that require a separate configuration file should place
a .cfg file in /etc/diamond/collectors.
The configuration file name should match the name of the diamond collector class 

"""
import diamond.collector

class ExampleCollector(diamond.collector.Collector):
    def get_default_config_help(self):
        config_help = super(ExampleCollector, self).get_default_config_help()

        config_help.update({    
        })

        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ExampleCollector, self).get_default_config()

        config.update({
            'path': 'example'
        })

        return config

    def collect(self):
        """
        Overrides the Collector.collect method
        """

        # Set Metric Name
        metric_name = "my.example.metric"

        # Set Metric Value
        metric_value = 42

        # Publish Metric
        self.publish(metric_name, metric_value)


