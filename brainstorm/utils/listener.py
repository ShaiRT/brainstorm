from .connection import Connection
import socket


class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        self.listener = None

    def __repr__(self):
        port = self.port
        host = self.host
        backlog = self.backlog
        reuseaddr = self.reuseaddr
        cls = self.__class__.__name__
        return f'{cls}({port=}, {host=!r}, {backlog=!r}, {reuseaddr=})'

    def start(self):
        if self.listener is not None:
            return
        self.listener = socket.socket()
        if self.reuseaddr:
            self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((self.host, self.port))
        self.listener.listen(self.backlog)

    def stop(self):
        if self.listener is not None:
            self.listener.close()
            self.listener = None

    def accept(self):
        if self.listener is None:
            return
        conn, addr = self.listener.accept()
        return Connection(conn)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception, error, traceback):
        self.stop()

