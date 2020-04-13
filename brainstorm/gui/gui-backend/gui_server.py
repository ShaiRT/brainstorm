import flask

gui_server = flask.Flask('brainstorm')

@gui_server.route('/')
def index():
	return flask.render_template('index.html', token='localhost:5000')

gui_server.run()