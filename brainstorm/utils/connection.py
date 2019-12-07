import socket


class Connection:
    def __init__(self, socket):
        self.socket = socket

    def __repr__(self):
        sock = self.socket.getsockname()
        peer = self.socket.getpeername()
        return f'<Connection from {sock[0]}:{sock[1]} to {peer[0]}:{peer[1]}>'

    def send(self, data):
        self.socket.sendall(data)

    def receive(self, size):
        data = b''

        # get data
        while True:
            new_data = self.socket.recv(1)
            data += new_data
            if not new_data:
                break
            if len(data) >= size:
                break

        # connection was closed before all the data was received
        if len(data) < size:
            raise Exception('Incomplete data: ' + data.decode('utf-8'))

        return data[:size]

    def close(self):
        self.socket.close()

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        self.close()

    def connect(host, port):
        sock = socket.socket()
        sock.connect((host, port))
        return Connection(sock)
