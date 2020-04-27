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
            assert clss.__name__ is 'Publisher' or clss.__name__ is 'Subscriber'
            assert name == clss.__name__.lower()


@pytest.fixture
def rabbitmq_url():
    return 'rabbitmq://127.0.0.1:9877'


@pytest.fixture
def connection_params(rabbitmq_url):
    url = furl.furl(rabbitmq_url)
    return pika.ConnectionParameters(host=url.host, port=url.port)


def test_publisher(rabbitmq_url, user, connection_params):
    publisher_class = mq_drivers['rabbitmq']['publisher']
    publisher = publisher_class(rabbitmq_url, 'test', 'fanout', 'test')
    user['birthday'] = user['birthday'].timestamp()
    publisher.publish(json.dumps(user))
    
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.exchange_declare(exchange='test', exchange_type='fanout')
    channel.queue_declare(queue='test')
    channel.queue_bind(exchange='test', queue='test', routing_key='test')
    channel.basic_qos(prefetch_count=1)

    def callback(channel, method, properties, data):
        channel.basic_ack(delivery_tag=method.delivery_tag)
        assert data.decode() == json.dumps(user)
        channel.close()

    channel.basic_consume(queue='test', on_message_callback=callback)
    channel.start_consuming()


def test_subscriber(rabbitmq_url, user, connection_params):
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    channel.exchange_declare(exchange='test', exchange_type='fanout')
    user['birthday'] = user['birthday'].timestamp()
    message = json.dumps(user)
    channel.basic_publish(exchange='test', routing_key='test', body=message)
    connection.close()

    def callback(message):
        assert message.decode() == json.dumps(user)

    subscriber_class = mq_drivers['rabbitmq']['subscriber']
    subscriber = subscriber_class(rabbitmq_url, 'test', 'fanout')
    subscriber.subscribe('test', callback, routing_key='test', just_one=True)


def test_publish_and_consume(rabbitmq_url):
    publisher = mq_drivers['rabbitmq']['publisher'](rabbitmq_url, 'test', 'fanout', 'test')
    subscriber = mq_drivers['rabbitmq']['subscriber'](rabbitmq_url, 'test', 'fanout')
    publisher.publish('hello')

    def callback(message):
        assert message == b'hello'

    subscriber.subscribe('test', callback, just_one=True)
