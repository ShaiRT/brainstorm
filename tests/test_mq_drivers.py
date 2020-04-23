import brainstorm.mq_drivers as mq_drivers
import furl
import inspect
import json
import pika
import pytest


def test_import():
    """Test the dynamic importing of the module
    """
    assert type(mq_drivers) == dict
    for key, classes in mq_drivers.items():
        assert type(classes) == dict
        for name, clss in classes.items():
            assert inspect.isclass(clss)
            assert clss.__name__ is 'Publisher' or clss.__name__ is 'Consumer'
            assert name == clss.__name__.lower()
'''
@pytest.fixture
def connection_params(rabbitmq):
    url = furl.furl(rabbitmq)
    return pika.ConnectionParameters(host=url.host, port=url.port)
'''

'''
def test_publish_and_consume(rabbitmq):
    publisher = mq_drivers['rabbitmq']['publisher'](rabbitmq, 'test', 'fanout', 'test')
    consumer = mq_drivers['rabbitmq']['consumer'](rabbitmq, 'test', 'fanout')
    publisher.publish('hello')
    consumer.consume('test', print)
'''
'''
def test_publisher(rabbitmq, user, connection_params):
    publisher_class = mq_drivers['rabbitmq']['publisher']
    publisher = publisher_class(rabbitmq, 'test', 'fanout', 'test')
    print('now publishing')
    user['birthday'] = user['birthday'].timestamp()
    publisher.publish(json.dumps(user))
    print('got publisher')
    connection = pika.BlockingConnection(connection_params)
    print('connected')
    channel = connection.channel()
    channel.exchange_declare(exchange='test', exchange_type='fanout')
    channel.queue_declare(queue='test')
    channel.queue_bind(exchange='test', queue='test', routing_key='test')
    channel.basic_qos(prefetch_count=1)
    recieved = dict()

    def on_message_callback(channel, method, properties, data):
        recieved['message'] = data
        channel.basic_ack(delivery_tag=method.delivery_tag)
        channel.close()

    channel.basic_consume(queue='test', on_message_callback=on_message_callback)
    channel.start_consuming()
    assert json.loads(recieved['message']) == user
    
        
'''
'''
class Publisher:

    def publish(self, message):
        connection = pika.BlockingConnection(self.params)
        channel = connection.channel()
        channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type)
        channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key, body=message)
        connection.close()


class Consumer:

    def __init__(self, url, exchange, exchange_type):
        self.url = furl.furl(url)
        self.params = pika.ConnectionParameters(host=self.url.host, port=self.url.port)
        self.exchange = exchange
        self.exchange_type = self.exchange_type    

    def consume(self, queue, callback, *, routing_key=''):
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
'''