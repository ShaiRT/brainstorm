import brainstorm.client as client
import brainstorm.client.reader as reader
import pytest
import requests
import bson


class MockReader():
    def __init__(self, path, driver):
        pass

    def __iter__(self):
        yield self.snapshot.copy()


@pytest.fixture
def mock_reader(user, snapshot, monkeypatch):
    MockReader.user = user
    MockReader.snapshot = snapshot
    monkeypatch.setattr(reader, 'Reader', MockReader)


def mock_post(url, data, headers):
    mock_requests.data = data
    class Response:
        status_code = 200

        def close(self):
            pass
    return Response()


@pytest.fixture
def mock_requests(monkeypatch):
    monkeypatch.setattr(requests, 'post', mock_post)
    return mock_requests


def test_user(mock_reader, mock_requests, user):
    client.upload_sample('.', host='localhost', port=8000)
    recieved_snapshot = bson.decode(mock_requests.data)
    assert recieved_snapshot['user'] == user


def test_snapshot(mock_reader, mock_requests, user, snapshot):
    client.upload_sample('.', host='localhost', port=8000)
    recieved_snapshot = bson.decode(mock_requests.data)
    del recieved_snapshot['user']
    assert recieved_snapshot == snapshot
