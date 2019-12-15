import contextlib
import multiprocessing
import pathlib
import signal
import socket
import subprocess
import sys
import threading
import time

import pytest



_SERVER_ADDRESS = '127.0.0.1', 5000
_SERVER_BACKLOG = 1000
_ROOT = pathlib.Path(__file__).absolute().parent.parent
_SERVER_PATH = _ROOT / 'brainstorm'
_CLIENT_PATH = _ROOT / 'brainstorm'

'''
def test_client():
    server = multiprocessing.Process(target=run_server)
    server.start()
    try:
        time.sleep(0.1)
        host, port = _SERVER_ADDRESS
        process = subprocess.Popen(
            ['python', _CLIENT_PATH, f'{host}:{port}', '1', "I'm hungry"],
            stdout = subprocess.PIPE,
        )
        stdout, _ = process.communicate()
        assert b'usage' in stdout.lower()
        process = subprocess.Popen(
            ['python', '-m', _CLIENT_PATH, 'upload-thought', f'address={host}:{port}', f'user=1', f"thought=I'm hungry"],
            stdout = subprocess.PIPE,
        )
        stdout, _ = process.communicate()
        assert b'done' in stdout.lower()
    finally:
        server.terminate()
'''

def run_server():
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(_SERVER_ADDRESS)
    server.listen(_SERVER_BACKLOG)
    try:
        while True:
            connection, address = server.accept()
            connection.close()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()

'''
def test_server():
    host, port = _SERVER_ADDRESS
    process = subprocess.Popen(
        ['python', _SERVER_PATH, f'{host}:{port}', 'data/'],
        stdout = subprocess.PIPE,
    )
    stdout, _ = process.communicate()
    assert b'usage' in stdout.lower()
    process = subprocess.Popen(
        ['python', _SERVER_PATH, 'run', f'address={host}:{port}', 'data=data/'],
        stdout = subprocess.PIPE,
    )
    thread = threading.Thread(target=process.communicate)
    thread.start()
    time.sleep(0.5)
    try:
        connection = socket.socket()
        connection.connect(_SERVER_ADDRESS)
        connection.close()
    finally:
        process.send_signal(signal.SIGINT)
        thread.join()
'''