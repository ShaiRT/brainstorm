import flask
import json
import click
from . import mongodb_driver as db_driver


api_server = flask.Flask('brainstorm')


@click.group()
def api_cli():
    pass


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
	return flask.jsonify(user)

@api_server.route('/users/<int:user_id>/snapshots')
def get_user_snapshots(user_id):
	db = api_server.config['db']
	snapshots = db.get_user_snapshots(user_id)
	return flask.jsonify(snapshots)

@api_server.route('/users/<int:user_id>/snapshots/<int:snapshot_id>')
def get_snapshot(user_id, snapshot_id):
	db = api_server.config['db']
	snapshot = db.get_snapshot(user_id, snapshot_id)
	if snapshot is None:
		return '', 404
	return flask.jsonify(snapshot)

@api_server.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>')
def get_snapshot_result(user_id, snapshot_id, result_name):
	db = api_server.config['db']
	result = db.get_snapshot_result(user_id, snapshot_id, result_name)
	if result is None:
		return '', 404
	if result_name in ['color_image', 'depth_image']:
		del result[result_name]['path']
	return flask.jsonify(result)

@api_server.route('/users/<int:user_id>/snapshots/<int:snapshot_id>/<result_name>/data')
def get_snapshot_result_data(user_id, snapshot_id, result_name):
	if result_name not in ['color_image', 'depth_image']:
		return '', 404
	db = api_server.config['db']
	result = db.get_snapshot_result(user_id, snapshot_id, result_name)
	if result is None:
		return '', 404
	return flask.send_file(result[result_name]['path'])


@api_cli.command('run-server')
@click.option('host', '-h', '--host', default='127.0.0.1', show_default=True)
@click.option('port', '-p', '--port', default=5000, show_default=True)
@click.option('database_url', '-d', '--database',
			  default='mongodb://localhost:27017', show_default=True)
def run_api_server(host='127.0.0.1', port=5000, database_url='mongodb://localhost:27017'):
    global api_server
    api_server.config['db'] = db_driver.Database(database_url)
    api_server.run(host=host, port=port, debug=False, threaded=True)


if __name__ == '__main__':
    api_cli()
