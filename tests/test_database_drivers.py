import brainstorm.database_drivers as db_drivers
import datetime as dt
import inspect
import pymongo
import pytest
import stringcase as sc


def test_import():
    """Test the dynamic importing of the module
    """
    assert type(db_drivers) == dict
    for key, val in db_drivers.items():
        assert inspect.isclass(val)
        assert val.__name__.endswith('Driver')
        assert key + '_driver' == sc.snakecase(val.__name__)


@pytest.fixture(scope='module')
def test_db(mongo):
	return db_drivers['mongodb'](mongo)


@pytest.fixture(scope='module')
def mongo_db(mongo):
	return pymongo.MongoClient(mongo).brainstorm


def test_save_user(mongo_db, test_db, user):
	test_db.save_user(user)
	db_user = list(mongo_db.users.find({'user_id': user['user_id']}))[0]
	assert user.items() <= db_user.items()
	assert db_user['snapshots_count'] == 0


def test_save_user_again(mongo_db, test_db, user):
	test_db.save_user(user)
	db_user = list(mongo_db.users.find({'user_id': user['user_id']}))
	assert len(db_user) == 1
	assert user.items() <= db_user[0].items()
	assert db_user[0]['snapshots_count'] == 0


def test_save_snapshot(mongo_db, test_db, user, snapshot_no_blobs):
	snapshot = snapshot_no_blobs
	snapshot['user_id'] = user['user_id']
	test_db.save_snapshot(snapshot)
	users = mongo_db.users
	snapshots = mongo_db.snapshots
	db_user = list(users.find({'user_id': user['user_id']}))[0]
	db_snapshot = list(snapshots.find({'datetime': snapshot['datetime']}))[0]
	assert snapshot.items() <= db_snapshot.items()
	assert db_snapshot['snapshot_id'] == 1
	assert db_user['snapshots_count'] == 1


def test_save_snapshot_again(mongo_db, test_db, user, snapshot_no_blobs):
	snapshot = snapshot_no_blobs
	snapshot['user_id'] = user['user_id']
	test_db.save_snapshot(snapshot)
	users = mongo_db.users
	snapshots = mongo_db.snapshots
	db_user = list(users.find({'user_id': user['user_id']}))[0]
	db_snapshot = list(snapshots.find({'datetime': snapshot['datetime']}))
	assert len(db_snapshot) == 1
	assert snapshot.items() <= db_snapshot[0].items()
	assert db_snapshot[0]['snapshot_id'] == 1
	assert db_user['snapshots_count'] == 1


def test_get_users(test_db, user):
	users = test_db.get_users()
	assert len(users) == 1
	assert users[0]['user_id'] == user['user_id']
	assert users[0]['username'] == user['username']


def test_get_user(test_db, user):
	db_user = test_db.get_user(user['user_id'])
	assert db_user == user


def test_get_snapshots(test_db, user, snapshot_no_blobs):
	snapshots = test_db.get_snapshots(user['user_id'])
	assert len(snapshots) == 1
	assert snapshots[0]['snapshot_id'] == 1
	assert snapshots[0]['datetime'] == snapshot_no_blobs['datetime']


def test_get_snapshot(test_db, user, snapshot_no_blobs):
	db_snapshot = test_db.get_snapshot(user['user_id'], 1)
	assert db_snapshot['snapshot_id'] == 1
	assert db_snapshot['datetime'] == snapshot_no_blobs['datetime']
	assert set(db_snapshot['available_results']) == set(['color_image', 'depth_image', 'feelings', 'pose'])


def test_get_partial_snapshot(test_db, user, snapshot_no_blobs):
	del snapshot_no_blobs['color_image']
	del snapshot_no_blobs['depth_image']
	snapshot_no_blobs['user_id'] = user['user_id']
	snapshot_no_blobs['datetime'] = dt.datetime(2020, 12, 12)
	test_db.save_snapshot(snapshot_no_blobs)
	db_snapshot = test_db.get_snapshot(user['user_id'], 2)
	assert db_snapshot['snapshot_id'] == 2
	assert db_snapshot['datetime'] == snapshot_no_blobs['datetime']
	assert set(db_snapshot['available_results']) == set(['feelings', 'pose'])


def test_get_result(test_db, user, snapshot_no_blobs):
	result = test_db.get_result(user['user_id'], 1, 'pose')
	assert result == snapshot_no_blobs['pose']
	result = test_db.get_result(user['user_id'], 1, 'feelings')
	assert result == snapshot_no_blobs['feelings']
	result = test_db.get_result(user['user_id'], 1, 'depth_image')
	assert result == snapshot_no_blobs['depth_image']
	result = test_db.get_result(user['user_id'], 1, 'color_image')
	assert result == snapshot_no_blobs['color_image']
