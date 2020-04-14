import flask
from pathlib import Path
import inspect
import os

root = Path(inspect.getsourcefile(lambda: 0)).absolute()
root = root.parent

gui_server = flask.Flask('brainstorm', root_path=root, static_folder="./gui-app/build/static", template_folder="./gui-app/build")

@gui_server.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(gui_server.root_path, 'gui-app/build'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@gui_server.route('/users')
@gui_server.route('/')
def index():
	return flask.render_template('index.html', api_url='localhost:5000')

gui_server.run()