from brainstorm.api.api import api_server
import pytest
import copy


class MockDB:
    def get_users(self):
        return [self.user]

    def get_user(self, user_id):
        return self.user

    def get_snapshots(self, user_id):
        return [self.snapshot]

    def get_snapshot(self, user_id, snapshot_id):
        return self.snapshot

    def get_result(self, user_id, snapshot_id, result):
        if result == 'fail':
            return None
        return self.snapshot[result]


@pytest.fixture
def mock_db(user, snapshot_no_blobs, monkeypatch):
    monkeypatch.setitem(api_server.config, 'db', MockDB())
    MockDB.snapshot = copy.deepcopy(snapshot_no_blobs)
    MockDB.user = user.copy()


def test_get_users(mock_db, user):
    response = api_server.test_client().get('/users')
    del user['birthday']
    assert response.status_code == 200
    assert type(response.json) == list
    assert len(response.json) == 1
    assert user.items() <= response.json[0].items()


def test_get_user(mock_db, user):
    response = api_server.test_client().get('/users/12')
    user['birthday'] = user['birthday'].strftime('%B %e, %Y')
    assert response.status_code == 200
    assert response.json == user


def test_get_snapshots(mock_db, snapshot_no_blobs):
    response = api_server.test_client().get('/users/12/snapshots')
    del snapshot_no_blobs['datetime']
    assert response.status_code == 200
    assert type(response.json) == list
    assert len(response.json) == 1
    assert snapshot_no_blobs.items() <= response.json[0].items()


def test_get_snapshot(mock_db, snapshot_no_blobs):
    del snapshot_no_blobs['datetime']
    response = api_server.test_client().get('/users/12/snapshots/1')
    assert response.status_code == 200
    assert snapshot_no_blobs.items() <= response.json.items()


def test_get_result_pose(mock_db, snapshot_no_blobs):
    del snapshot_no_blobs['datetime']
    response = api_server.test_client().get('/users/12/snapshots/1/pose')
    assert response.status_code == 200
    assert snapshot_no_blobs['pose'] == response.json


def test_get_result_color_image(mock_db, snapshot_no_blobs):
    del snapshot_no_blobs['datetime']
    response = api_server.test_client().get('/users/12/snapshots/1/color_image')
    color_image = snapshot_no_blobs['color_image']
    color_image['data_url'] = '/users/12/snapshots/1/color_image/data'
    assert response.status_code == 200
    assert snapshot_no_blobs['color_image'] == response.json


def test_get_result_fail(mock_db):
    response = api_server.test_client().get('/users/12/snapshots/1/fail')
    assert response.status_code == 404
    assert b'' == response.data


def test_get_data_fail(mock_db):
    response = api_server.test_client().get('/users/12/snapshots/1/pose/data')
    assert response.status_code == 404
    assert b'' == response.data
