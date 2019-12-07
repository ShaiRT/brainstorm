import time
import struct
import threading
from pathlib import Path
from .utils import Listener
import click


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
                header = self.conn.receive(20)
                user_id, time_stamp, thought_size = \
                    struct.unpack('QQI', header)
                thought = self.conn.receive(thought_size).decode('utf-8')
                time_format = '%Y-%m-%d_%H-%M-%S'
                tm = time.localtime(time_stamp)
                time_stamp = time.strftime(time_format, tm) + '.txt'
                path = Path('.') / self.data_dir / str(user_id)

                # save thought in file
                with self.lock:
                    path.mkdir(parents=True, exist_ok=True)
                    path = path / time_stamp
                    if not path.exists():
                        path.touch()
                    else:
                        thought = '\n' + thought
                    with path.open(mode='a+') as f:
                        f.write(thought)

        except Exception as error:
            if not error.__str__() == 'Incomplete data: ':
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
