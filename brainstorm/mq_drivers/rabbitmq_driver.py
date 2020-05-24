"""Rabbitmq message queue driver with Publisher and Subscriber
"""
import furl
import pika


class Publisher:

    def __init__(self, url, exchange, exchange_type='fanout', routing_key=''):
        '''
        Arguments:
            url {str} -- message queue url
            exchange {str} -- exchange name
        
        Keyword Arguments:
            exchange_type {str} -- exchange type (default: {'fanout'})
            routing_key {str} -- routing key (default: {''})
        '''
        self.url = furl.furl(url)
        self.params = pika.ConnectionParameters(host=self.url.host, port=self.url.port)
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.routing_key = routing_key

    def publish(self, message):
        """publish message to the message queue
        in the self.exchange with self.routing_key
        
        Args:
            message (str): the message to be published
        """
        connection = pika.BlockingConnection(self.params)
        channel = connection.channel()
        channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type)
        channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key, body=message)
        connection.close()


class Subscriber:

    def __init__(self, url, exchange, exchange_type='fanout'):
        '''
        Arguments:
            url {str} -- message queue url
            exchange {str} -- exchange name
        
        Keyword Arguments:
            exchange_type {str} -- exchange type (default: {'fanout'})
        '''
        self.url = furl.furl(url)
        self.params = pika.ConnectionParameters(host=self.url.host, port=self.url.port)
        self.exchange = exchange
        self.exchange_type = exchange_type    

    def subscribe(self, queue, callback, *, routing_key='#', just_one=False):
        '''Consume messages from given queue in self.exchange with
        given routing key. use callback to handle the messages.
        This function doesn't return (consumes forever),
        unless just_one == True, in which case only one message is consumed.
        
        Arguments:
            queue {str} -- name of queue to consume
            callback {function} -- callback to handle messages
        
        Keyword Arguments:
            routing_key {str} -- routing key to filter messages (default: {'#'})
            just_one {bool} -- consume only one message (default: {False})
        '''
        connection = pika.BlockingConnection(self.params)
        channel = connection.channel()
        channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type)
        channel.queue_declare(queue=queue)
        channel.queue_bind(exchange=self.exchange, queue=queue, routing_key=routing_key)
        channel.basic_qos(prefetch_count=1)

        def on_message_callback(channel, method, properties, data):
            callback(data)
            channel.basic_ack(delivery_tag=method.delivery_tag)
            if just_one:
                channel.close()

        channel.basic_consume(queue=queue, on_message_callback=on_message_callback)
        channel.start_consuming()
