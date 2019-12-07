from .utils import Connection
from .thought import Thought
import datetime as dt
import click


@click.argument('address')
@click.argument('user_id', type=click.INT)
@click.argument('thought')
def upload_thought(address, user_id, thought):
    ip, port = address.split(':')
    address = (ip, int(port))
    timestamp = dt.datetime.now()
    thought = Thought(user_id, timestamp, thought)
    with Connection.connect(*address) as conn:
        conn.send(thought.serialize())
