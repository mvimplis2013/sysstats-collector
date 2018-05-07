# coding=utf-8

"""
Output the collected values to RabbitMQ Topic Exchange.
This allows for 'subscribing' to messages beased on the routing key, which is the metric path 
"""

from Handler import Handler

try:
    import pika
except ImportError:
    pika = None

class rmqHandler(Handler):
    """
    Implements the abstract Handler class.
    Sending data to a RabbitMQ topic exchange.
    The routing key will be the full name of the metric being sent.

    Based on the rmqHandler and zmqHandler code.
    
    Arguments:
        Handler {[type]} -- [description]
    """

    def __init__(self, config):
        """
        Create a new instance of rmqHandler class
        
        Arguments:
            config {[type]} -- [description]
        """

        # Initialize Handler
        Handler.__init__(self, config)

        # Initialize Data
        self.connection = None
        self.channel = None

        # Initialize Options
        # self.server = self.config.get('server', '127.0.0.1')
        self.server = '127.0.0.1'
        self.port = self.config.get('port', 5672)
        self.topic_exchange = self.config.get('topic_exchange', 'diamond')
        self.vhost = self.config.get('vhost', '')
        self.user = self.config.get('user', 'guest')
        self.password = self.config.get('password', 'guest')
        self.routing_key = self.config.get('routing_key', 'metric')
        self.custom_routing_key = self.config.get('custom_routing_key', 'diamond')

        print('host', self.server)
        if not pika:
            self.log.error('pika import failed. Handler disabled')
            self.enabled = False
            return

        # Create rabbitMQ topic exchange and bind
        try:
            self._bind()

        except pika.exceptions.AMQPConnectionError:
            self.log.error("Failed to bind to rabbitMQ topic exchange")

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler.
        """
        config = super(rmqHandler, self).get_default_config_help()

        config.update({
            'server': '',
            'topic_exchange': '',
            'vhost': '',
            'user': '',
            'password': '',
            'routing_key': '',
            'custom_routing_key': '',
        })

        return config

    def get_default_config(self):
        """
        Returns the default configuration for this handler
        """

        config = super(rmqHandler, self).get_default_config()

        config.update({
            'server': '127.0.0.1',
            'topic_exchange': 'diamond',
            'vhost': '/',
            'user': 'guest',
            'password': 'guest',
            'port': '5672',
        })

        return config

    def _bind(self):
        """
        Create socket and bind
        """
        credentials = pika.PlainCredentials(self.user,  self.password)
        print('host', self.server)
        params = pika.ConnectionParameters(credentials=credentials, host=self.server, virtual_host=self.vhost, port=self.port)

        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

        # NOTE: PIKA version uses 'exchange_type' instead of 'type'
        self.channel.exchange_declare(exchange=self.topic_exchange, exchange_type="topic")

    def __del__(self):
        """
        Destroy instance of the rmqHandler class
        """
        try:
            self.connection.close()
        except AttributeError:
            pass

    def process(self, metric):
        """
        Process a metric and send it to RabbitMQ topic exchange
        
        Arguments:
            metric {[type]} -- [description]
        """
        # Senmd the data as ...
        if not pika:
            return

        routingKeyDic = {
            'metric': lambda: metric.path,
            'custom': lambda: self.cutom_routing_key,

            # These option and the below are really not needed as 
            # with Rabbitmq you can use regular expressions to indicate
            # what routing_keys to subscribe to. THis is a good example
            # of how to allow more routing keys

            'host': lambda: metric.host,
            'metric.path': metric.getMetricPath,
            'path.prefix': metric.getPathPrefix,
            'collector.path': metric.getCollectorPath,

        }

        try:
            self.channel.basic_publish(
                exchange=self.topic_exchange,
                routing_key=routingKeyDic[self.routing_key](),
                body="%s" % metric
            )

        except Exception as e:  # Rough connection re-try logic
            self.log.info("Failed publishing to rabbitMQ. Attempting reconnect")
            self._bind()



