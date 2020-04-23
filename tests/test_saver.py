import brainstorm.database_drivers as db_drivers
import brainstorm.saver as saver
import json
import pytest


class MockDBDriver:
    def __init__(self, url):
        pass

    def save_user(self, user):
        MockDBDriver.user = user

    def save_snapshot(self, snapshot):
        MockDBDriver.snapshot = snapshot


@pytest.fixture
def mock_db(monkeypatch):
    monkeypatch.setitem(db_drivers, 'mock', MockDBDriver)


def test_saver(mock_db, user, snapshot_no_blobs):
    snapshot = snapshot_no_blobs.copy()
    snapshot['user'] = user.copy()
    snapshot['user']['birthday'] = user['birthday'].timestamp()
    snapshot['datetime'] = snapshot['datetime'].timestamp() * 1000
    my_saver = saver.Saver('mock://localhost:1234')
    my_saver.save(json.dumps(snapshot))
    snapshot_no_blobs['user_id'] = user['user_id']
    assert MockDBDriver.user == user
    assert MockDBDriver.snapshot == snapshot_no_blobs


def test_save_from_path(mock_db, tmp_path, user, snapshot_no_blobs):
    snapshot = snapshot_no_blobs.copy()
    snapshot['user'] = user.copy()
    snapshot['user']['birthday'] = user['birthday'].timestamp()
    snapshot['datetime'] = snapshot['datetime'].timestamp() * 1000
    (tmp_path / 'data').write_text(json.dumps(snapshot))
    saver.save_from_path('mock://localhost:1234', str(tmp_path / 'data'))
    snapshot_no_blobs['user_id'] = user['user_id']
    assert MockDBDriver.user == user
    assert MockDBDriver.snapshot == snapshot_no_blobs
