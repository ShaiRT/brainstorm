import time
import struct
import threading
from pathlib import Path
from .utils import Listener
import click
from .utils import parser, Context
from .utils import Snapshot, Hello, Config


class Handler(threading.Thread):
    '''
    handler for a client that connected to server
    '''
    lock = threading.Lock()

    def __init__(self, conn, data_dir):
        super().__init__()
        self.conn = conn
        self.data_dir = data_dir

    def run(self):  # invoked by start
        '''
        Recieves data from client and saves it in file
        raises exception for incomplete data
        '''
        try:
            while True:
                hello = Hello.deserialize(self.conn.recieve_message())
                user_id = hello.user_id
                config = Config(parser.fields.keys())
                self.conn.send_message(config.serialize())
                snapshot = Snapshot.deserialize(self.conn.recieve_message())
                time_stamp = snapshot.datetime
                time_format = '%Y-%m-%d_%H-%M-%S-%f'
                time_stamp = time_stamp.strftime(time_format)
                path = Path('.') / self.data_dir / str(user_id) / time_stamp
                context = Context(path)
                with self.lock:
                    path.mkdir(parents=True, exist_ok=True)
                    for field, f in parser.fields.items():
                        f(context, snapshot)

        except Exception as error:
            if not error.__str__().startswith('Incomplete data'):
                raise error
        finally:
            self.conn.close()


class Server:
    def __init__(self, address, data_dir):
        self.address = address
        self.data_dir = data_dir

    def start(self):
        '''
        Run server that listens on address
        creates a new Handler for each client
        '''
        ip, port = self.address
        with Listener(port, ip) as listener:
            while True:
                conn = listener.accept()
                handler = Handler(conn, self.data_dir)
                handler.start()


@click.argument('address')
@click.argument('data_dir')
def run_server(address, data_dir):
    ip, port = address.split(':')
    address = (ip, int(port))
    server = Server(address, data_dir)
    server.start()
