import click
from brainstorm.parsers.__init__ import parse
import furl
import pika
import functools as ft


@click.group()
def parsers_cli():
    pass


@parsers_cli.command('parse')
@click.argument('name')
@click.argument('path')
def parse_path(name, path):
    global parsers
    with open(path, 'rb') as f:
        data = f.read()
    return parse(name, data)


def parse_and_publish(receiving_channel, method, properties,
                      data, *, host, port, parser):
    params = pika.ConnectionParameters(host=host, port=port)
    connection = pika.BlockingConnection(params)
    publishing_channel = connection.channel()
    publishing_channel.exchange_declare(exchange='data', exchange_type='topic')
    data = parse(parser, data)
    publishing_channel.basic_publish(exchange='data',
                                     routing_key=parser, body=data)
    connection.close()
    receiving_channel.basic_ack(delivery_tag=method.delivery_tag)


@parsers_cli.command()
@click.argument('name')
@click.argument('url')
def run_parser(name, url):
    f = furl.furl(url)
    host = f.host
    port = f.port
    params = pika.ConnectionParameters(host=host, port=port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange='snapshots', exchange_type='fanout')
    channel.queue_declare(queue=name)
    channel.queue_bind(exchange='snapshots', queue=name)
    channel.basic_qos(prefetch_count=1)
    callback = ft.partial(parse_and_publish, host=host, port=port, parser=name)
    channel.basic_consume(queue=name, on_message_callback=callback)
    channel.start_consuming()


parsers_cli()
