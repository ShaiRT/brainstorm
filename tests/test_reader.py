import brainstorm.client.reader_drivers as drivers
import pytest

from brainstorm.client import Reader


class MockDriver():
    def __init__(self, path):
        self._count = 0

    def get_user(self):
        return self.user

    def get_snapshot(self):
        self._count += 1
        return self.snapshot if self._count == 1 else None


@pytest.fixture
def mock_drivers(user, snapshot, monkeypatch):
    MockDriver.user = user
    MockDriver.snapshot = snapshot
    monkeypatch.setitem(drivers, 'mock', MockDriver)


def test_attributes(mock_drivers, user):
    reader = Reader('', driver='mock')
    assert reader.user_id == user['user_id']
    assert reader.username == user['username']


def test_iter(mock_drivers, snapshot):
    reader = Reader('', driver='mock')
    assert len(list(iter(reader))) == 1
    reader = Reader('', driver='mock')
    assert next(iter(reader)) == snapshot
