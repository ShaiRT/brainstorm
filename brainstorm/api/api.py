import flask
import furl
import os

import brainstorm.database_drivers as db_drivers

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


@api_server.route("/shutdown", methods=['POST'])
def shutdown_server():
    # TODO: add username and password for shutdown?
    shutdown = flask.request.environ.get('werkzeug.server.shutdown')
    if shutdown is None:
        raise RuntimeError('server shutdown failed')
    shutdown()
    return '', 200


@api_server.route('/users')
def get_users():
    db = api_server.config['db']
    users = db.get_users()
    return flask.jsonify(users)


@api_server.route('/users/<int:user_id>')
def get_user(user_id):
    db = api_server.config['db']
    user = db.get_user(user_id)
    if user is None:
        return '', 404
    user['birthday'] = user['birthday'].strftime('%B %e, %Y')
    return flask.jsonify(user)


@api_server.route('/users/<int:user_id>/snapshots')
def get_snapshots(user_id):
    db = api_server.config['db']
    snapshots = db.get_snapshots(user_id)
    for snapshot in snapshots:
        snapshot['datetime'] = snapshot['datetime'].strftime(
            '%H:%M:%S.%f')[:-3] + snapshot['datetime'].strftime(' %a, %b%e, %Y')
    return flask.jsonify(snapshots)


@api_server.route('/users/<int:user_id>/snapshots/<int:snapshot_id>')
def get_snapshot(user_id, snapshot_id):
    db = api_server.config['db']
    snapshot = db.get_snapshot(user_id, snapshot_id)
    if snapshot is None:
        return '', 404
    snapshot['datetime'] = snapshot['datetime'].strftime(
        '%H:%M:%S.%f')[:-3] + snapshot['datetime'].strftime(' %a, %b%e, %Y')
    return flask.jsonify(snapshot)


@api_server.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>')
def get_result(user_id, snapshot_id, result_name):
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
    if result_name not in ['color_image', 'depth_image']:
        return '', 404
    db = api_server.config['db']
    result = db.get_result(user_id, snapshot_id, result_name)
    if result is None:
        return '', 404
    return flask.send_file(result['path'])


def run_api_server(host='127.0.0.1', port=5000, database_url='mongodb://localhost:27017'):
    global api_server
    api_server.config['db'] = db_drivers[furl.furl(database_url).scheme](database_url)
    api_server.run(host=host, port=port, debug=False, threaded=True)
