import flask
import furl
import inspect
import os

from pathlib import Path


'''
# this code will suppress flask messages:
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
'''
os.environ['WERKZEUG_RUN_MAIN'] = 'true'


root = Path(inspect.getsourcefile(lambda: 0)).absolute()
root = root.parent

gui_server = flask.Flask('brainstorm', root_path=root, static_folder="./gui-app/build/static", template_folder="./gui-app/build")


@gui_server.route('/users')
@gui_server.route('/')
def index():
	return flask.render_template('index.html', api_url=gui_server.config['api_url'])


@gui_server.route('/users/<int:user_id>')
@gui_server.route('/users/<int:user_id>/snapshots')
def index_user(user_id):
    return flask.render_template('index.html', api_url=gui_server.config['api_url'])


@gui_server.route('/users/<int:user_id>/snapshots/<int:snapshot_id>')
def index_snapshot(user_id, snapshot_id):
    return flask.render_template('index.html', api_url=gui_server.config['api_url'])


@gui_server.route('/<path:path>')
def static_file(path):
    return flask.send_from_directory(os.path.join(gui_server.root_path, 'gui-app/build'), path)


def run_server(host='127.0.0.1', port=8080, api_host='127.0.0.1', api_port=5000):
    global gui_server
    api_url = furl.furl(host=api_host, port=api_port, scheme='http').url
    gui_server.config['api_url'] = api_url
    gui_server.run(host=host, port=port, debug=False, threaded=True)
