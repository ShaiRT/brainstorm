import brainstorm.database_drivers as db_drivers
import flask
import furl
import os

from flask_cors import CORS


os.environ['WERKZEUG_RUN_MAIN'] = 'true'
api_server = flask.Flask('brainstorm')
CORS(api_server)


@api_server.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


@api_server.route('/users')
def get_users():
    '''get a list all users in the database
    triggered when '/users' route is requested (with GET)
    
    Returns:
        string -- a list of users in json format
    '''
    db = api_server.config['db']
    users = db.get_users()
    return flask.jsonify(users)


@api_server.route('/users/<int:user_id>')
def get_user(user_id):
    '''get a specific user from the database
    triggeres when '/users/<int:user_id>' route is requested (with GET)
    
    Args:
        user_id (int): the requested user id
    
    Returns:
        string -- the requested user's information (or 404 if no such user)
    '''
    db = api_server.config['db']
    user = db.get_user(user_id)
    if user is None:
        return '', 404
    user['birthday'] = user['birthday'].strftime('%B %e, %Y')
    return flask.jsonify(user)


@api_server.route('/users/<int:user_id>/snapshots')
def get_snapshots(user_id):
    '''get a list all snapshot of a certain user from the database
    triggered when '/users/<int:user_id>/snapshots' route is requested (with GET)
    
    Args:
        user_id (int): the requested user id
    
    Returns:
        string -- list of snapshots in json format (empty list if user doesn't exist or has no snapshots)
    '''
    db = api_server.config['db']
    snapshots = db.get_snapshots(user_id)
    for snapshot in snapshots:
        snapshot['datetime'] = snapshot['datetime'].strftime(
            '%H:%M:%S.%f')[:-3] + snapshot['datetime'].strftime(' %a, %b%e, %Y')
    return flask.jsonify(snapshots)


@api_server.route('/users/<int:user_id>/snapshots/<int:snapshot_id>')
def get_snapshot(user_id, snapshot_id):
    '''get a specific snapshot by user snapshot id from the database
    triggered when '/users/<int:user_id>/snapshots/<int:snapshot_id>' route is requested (with GET)
    
    Args:
        user_id (int): id of requested user
        snapshot_id (int): id of requested snapshot
    
    Returns:
        string -- the requested snapshot (404 if it doesn't exist)
    '''
    db = api_server.config['db']
    snapshot = db.get_snapshot(user_id, snapshot_id)
    if snapshot is None:
        return '', 404
    snapshot['datetime'] = snapshot['datetime'].strftime(
        '%H:%M:%S.%f')[:-3] + snapshot['datetime'].strftime(' %a, %b%e, %Y')
    return flask.jsonify(snapshot)


@api_server.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>')
def get_result(user_id, snapshot_id, result_name):
    '''get a specific result of a snapshot by snapshot and user id from database
    triggered when '/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>' route is requested (with GET)
    
    Args:
        user_id (int): id of requested user
        snapshot_id (int): id of requested snapshot
        result_name (string): name of requested result
    
    Returns:
        string -- the requested result in json format (404 if no such result)
    '''
    db = api_server.config['db']
    result = db.get_result(user_id, snapshot_id, result_name)
    if result is None:
        return '', 404
    if result_name in ['color_image', 'depth_image']:
        result.pop('path', None)
        result['data_url'] = f'/users/{user_id}/snapshots/{snapshot_id}/{result_name}/data'
    return flask.jsonify(result)


@api_server.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>/data')
def get_result_data(user_id, snapshot_id, result_name):
    '''get a specific result's data of a snapshot by snapshot and user id from database
    triggered when '/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>/data' route is requested (with GET)
    
    Args:
        user_id (int): id of requested user
        snapshot_id (int): id of requested snapshot
        result_name (string): name of requested result
    
    Returns:
        requested data (image) or 404 if data doesn't exist
    '''
    if result_name not in ['color_image', 'depth_image']:
        return '', 404
    db = api_server.config['db']
    result = db.get_result(user_id, snapshot_id, result_name)
    if result is None:
        return '', 404
    return flask.send_file(result['path'])


def run_api_server(host='127.0.0.1', port=5000, database_url='mongodb://localhost:27017'):
    '''Run the api server to respond to http requests at 'http://host:port' and expose the data in the database.
    
    Args:
        host (str): the servers host (default: {'127.0.0.1'})
        port (int): the servers port (default: {5000})
        database_url (str): the url of the database (default: {'mongodb://localhost'})
    '''
    global api_server
    api_server.config['db'] = db_drivers[furl.furl(database_url).scheme](database_url)
    api_server.run(host=host, port=port, debug=False, threaded=True)
