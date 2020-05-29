import furl

from brainstorm.cli.__main__ import cli
from click.testing import CliRunner


URL = furl.furl(scheme='http', host='127.0.0.1', port=5000).url


def test_get_users(requests_mock, user):
    del user['birthday']
    del user['gender']
    requests_mock.get(URL + '/users', json=[user])
    runner = CliRunner()
    result = runner.invoke(cli, ['get-users'])
    assert user['username'] in result.output
    assert str(user['user_id']) in result.output


def test_get_user(requests_mock, user):
    user['birthday'] = user['birthday'].strftime('%B %e, %Y')
    requests_mock.get(URL + f"/users/{user['user_id']}", json=user)
    runner = CliRunner()
    result = runner.invoke(cli, ['get-user', str(user['user_id'])])
    assert user['username'] in result.output
    assert str(user['user_id']) in result.output
    assert user['gender'] in result.output
    assert user['birthday'] in result.output


def test_get_snapshots(requests_mock, snapshot_no_blobs):
    snapshot = {'snapshot_id': 1}
    snapshot['datetime'] = snapshot_no_blobs['datetime'].strftime(
        '%H:%M:%S.%f')[:-3] + \
        snapshot_no_blobs['datetime'].strftime(' %a, %b%e, %Y')
    requests_mock.get(URL + f"/users/1/snapshots", json=[snapshot])
    runner = CliRunner()
    result = runner.invoke(cli, ['get-snapshots', '1'])
    assert str(snapshot['snapshot_id']) in result.output
    assert snapshot['datetime'] in result.output


def test_get_snapshot(requests_mock, snapshot_no_blobs):
    snapshot = {'snapshot_id': 1}
    snapshot['datetime'] = snapshot_no_blobs['datetime'].strftime(
        '%H:%M:%S.%f')[:-3] + \
        snapshot_no_blobs['datetime'].strftime(' %a, %b%e, %Y')
    snapshot['available_results'] = list(snapshot_no_blobs.keys())
    requests_mock.get(URL + f"/users/1/snapshots/1", json=snapshot)
    runner = CliRunner()
    result = runner.invoke(cli, ['get-snapshot', '1', '1'])
    assert str(snapshot['snapshot_id']) in result.output
    assert snapshot['datetime'] in result.output
    for r in snapshot['available_results']:
        assert r in result.output


def test_get_result_pose(requests_mock, snapshot_no_blobs):
    pose = snapshot_no_blobs['pose']
    requests_mock.get(URL + f"/users/1/snapshots/1/pose", json=pose)
    runner = CliRunner()
    result = runner.invoke(cli, ['get-result', '1', '1', 'pose'])
    for key, val in pose.items():
        assert f'{key}: {val}' in result.output


def test_get_result_feelinga(requests_mock, snapshot_no_blobs):
    feelings = snapshot_no_blobs['feelings']
    requests_mock.get(URL + f"/users/1/snapshots/1/feelings", json=feelings)
    runner = CliRunner()
    result = runner.invoke(cli, ['get-result', '1', '1', 'feelings'])
    for key, val in feelings.items():
        assert f'{key}: {val}' in result.output
