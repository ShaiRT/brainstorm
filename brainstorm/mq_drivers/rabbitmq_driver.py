"""Rabbitmq message queue driver with Publisher and Consumer
"""
import furl
import pika


class Publisher:

    def __init__(self, url, exchange, exchange_type, routing_key):
        """
        Args:
            url (str): message queue url
            exchange (str): exchange name
            exchange_type (str): exchange type
            routing_key (str): routing key
        """
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


class Consumer:

    def __init__(self, url, exchange, exchange_type):
        """
        Args:
            url (str): message queue url
            exchange (str): exchange name
            exchange_type (str): exchange type
        """
        self.url = furl.furl(url)
        self.params = pika.ConnectionParameters(host=self.url.host, port=self.url.port)
        self.exchange = exchange
        self.exchange_type = exchange_type    

    def consume(self, queue, callback, *, routing_key='#'):
        """Consume message from given queue in self.exchange with
        given routing key. use callback to handle the messages.
        
        Args:
            queue (str): name of queue to consume
            callback (function): callback to handle messages
            routing_key (str, optional): routing key to filter messages
        """
        connection = pika.BlockingConnection(self.params)
        channel = connection.channel()
        channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type)
        channel.queue_declare(queue=queue)
        channel.queue_bind(exchange=self.exchange, queue=queue, routing_key=routing_key)
        channel.basic_qos(prefetch_count=1)

        def on_message_callback(channel, method, properties, data):
            callback(data)
            channel.basic_ack(delivery_tag=method.delivery_tag)

        channel.basic_consume(queue=queue, on_message_callback=on_message_callback)
        channel.start_consuming()
