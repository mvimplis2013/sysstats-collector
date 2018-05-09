# coding=utf-8

"""
Insert the collected values into a mysql table
"""

from diamond.handler.Handler import Handler

import pymysql

class MySQLHandler(Handler):
    """
    Implements the abstract Handler class, sending data to a mysql table
    
    Arguments:
        Handler {[type]} -- [description]
    """
    conn = None

    def __init__(self, config=None):
        """
        Create a new instance of the MySQLHandler class
        
        Keyword Arguments:
            config {[type]} -- [description] (default: {None})
        """
        # Initialize Handler
        Handler.__init__(self, config)

        # Initialize Options
        self.hostname = self.config['hostname']
        self.port = self.config['port']
        self.username = self.config['username']
        self.password = self.config['password']
        self.database = self.config['database']
        self.table = self.config['table']
        self.col_time = self.config['col_time']
        self.col_metric = self.config['col_metric']
        self.col_value = self.config['col_value']

        # Connect
        self._connect()

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options in this handler
        
        Returns:
            [type] -- [description]
        """

        config = super(MySQLHandler, self).get_default_config_help()

        config.update({            
        }) 

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """

        config = super(MySQLHandler, self).get_default_config()

        config.update({
        })

        return config
    
    def __del__(self):
        """
        Destroy instance of the MySQLHandler  
        """
        self.close()

    def process(self, metric):
        """
        Process a mnetric
        
        Arguments:
            metric {[type]} -- [description]
        """

        # Just send the data 
        self._send( str(metric) )

    def _send(self, data):
        """
        Insert the data 
        
        Arguments:
            metric {[type]} -- [description]
        """

        data = data.strip().split(' ')

        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO %s (%s, %s, %s) VALUES(%%s, %%s, %%s)"
                    % (self.table, self.col_metric, self.col_time, self.col_value),
                    (data[0], data[2], data[1]))
            cursor.close()
            self.conn.commit()             
        except BaseException as ex:
            # Log Error
            self.log.error("MySQLHandler: Failed sending data. %s.", ex)
            # Attempt to restablish connection
            self._connect()

    def _connect(self):
        """
        Connect to the MySQL server
        """
        try:
            self._close()
            self.conn = pymysql.connect(
                host=self.hostname, 
                port=self.port, 
                user=self.username, 
                password=self.password, 
                db=self.database)
        except Exception as e:
            self.log.error( e )

    def _close(self):
        """
        Close the connection
        """
        if self.conn:
            self.conn.commit()
            self.conn.close()


