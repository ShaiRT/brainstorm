"""A saver to save messages from the message queue to the database
"""
import brainstorm.database_drivers as db_drivers
import brainstorm.mq_drivers as mq_drivers
import datetime as dt
import furl
import json


class Saver:

    def __init__(self, database_url):
        """
        Args:
            database_url (str): the url of the database
        """
        driver = furl.furl(database_url).scheme
        self.db = db_drivers[driver](database_url)

    def save(self, data):
        """Save data to the savers database
        
        Args:
            data (str): data in json format
        """
        snapshot = json.loads(data)
        user = snapshot['user']
        del snapshot['user']
        snapshot['user_id'] = user['user_id']
        snapshot['datetime'] = dt.datetime.fromtimestamp(snapshot['datetime'] / 1000.0)
        user['birthday'] = dt.datetime.fromtimestamp(user['birthday'])
        self.db.save_user(user)
        self.db.save_snapshot(snapshot)


def save_from_path(database_url, path):
    """Save data in path to database in given url
    
    Args:
        database_url (str): the url of the database
        path (str): path to a file with json format content
    """
    with open(path, 'r') as f:
        data = f.read()
    saver = Saver(database_url)
    saver.save(data)


def run_saver(database_url, mq_url):
    """Run the saver to save mwssages from message queue.
    Saver saves all messages in 'data' topic exchange.
    
    Args:
        database_url (str): url of the database
        mq_url (str): url of the message queue
    """
    saver = Saver(database_url)
    consumer_class = mq_drivers[furl.furl(mq_url).scheme]['consumer']
    consumer = consumer_class(mq_url, 'data', 'topic')
    consumer.consume('save', saver.save, routing_key='#')
