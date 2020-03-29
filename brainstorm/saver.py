import pika
import pymongo
import json
import datetime as dt
import click
import furl


class Saver:
    def __init__(self, database_url):
        self.database_url = database_url
        self.client = pymongo.MongoClient(database_url)
        self.db = self.client.brainstorm
        self.users = self.db.users
        self.snapshots = self.db.snapshots

    def save(self, field, data):
        data = json.loads(data)
        user = data['user']
        del data['user']
        data['user_id'] = user['user_id']
        data['datetime'] = dt.datetime.fromtimestamp(data['datetime'] / 1000.0)
        user['birthday'] = dt.datetime.fromtimestamp(user['birthday'])
        self.users.update_one({'user_id': user['user_id']},
                              {'$set': user}, upsert=True)
        snapshot_filter = {'user_id': user['user_id'],
                           'datetime': data['datetime']}
        self.snapshots.update_one(snapshot_filter, {'$set': data}, upsert=True)


@click.group()
def saver_cli():
    pass


@saver_cli.command('save')
@click.option('database_url', '-d', '--database',
              default='mongodb://localhost:27017/', show_default=True)
@click.argument('field')
@click.argument('path')
def save_from_path(database_url, field, path):
    with open(path, 'r') as f:
        data = f.read()
    saver = Saver(database_url)
    saver.save(field, data)


@saver_cli.command()
@click.argument('database_url')
@click.argument('mq_url')
def run_saver(database_url, mq_url):
    saver = Saver(database_url)
    mq_url = furl.furl(mq_url)
    mq_host = mq_url.host
    mq_port = mq_url.port
    params = pika.ConnectionParameters(host=mq_host, port=mq_port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange='data', exchange_type='topic')
    channel.queue_declare(queue='save')
    channel.queue_bind(exchange='data',
                       queue='save', routing_key='#')
    channel.basic_qos(prefetch_count=1)

    def callback(channel, method, properties, data):
        saver.save(method.routing_key, data)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='save', on_message_callback=callback)
    channel.start_consuming()


if __name__ == '__main__':
    saver_cli()
