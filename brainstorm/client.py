from .utils import Connection
from .thought import Thought
import datetime as dt
import click
from .utils import Reader, Snapshot, Config, Hello


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

@click.argument('path')
@click.argument('port', type=click.INT)
def run_client(path, port):
	ip = '0.0.0.0'
	reader = Reader(path)
	hello = reader.hello
	for snapshot in reader:
		with Connection.connect(ip, port) as conn:
			conn.send_message(hello.serialize())
			config = Config.deserialize(conn.recieve_message())
			conn.send_message(snapshot.serialize())
