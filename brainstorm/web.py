from pathlib import Path
import click
import time
import flask

data_dir = ''
website = flask.Flask(__name__)

_INDEX_HTML = '''
<!-- INDEX-HTML -->
<html>
    <head>
        <title>Brain Computer Interface</title>
    </head>
    <body>
        <ul>
            {users}
        </ul>
    </body>
</html>
'''

_USER_LINE_HTML = '''
<!-- USER-LINE-HTML -->
<li><a href="/users/{user_id}">user {user_id}</a></li>
'''

_USER_HTML = '''
<!-- USER-HTML -->
<html>
    <head>
        <title>Brain Computer Interface: User {user}</title>
    </head>
    <body>
        <table>
            {files}
        </table>
    </body>
</html>
'''

_FILE_LINE_HTML = '''
<!-- FILE_LINE-HTML -->
<tr>
    <td>{time_stamp}</td>
    <td>{thought}</td>
</tr>
'''


def format_time_stamp(ts):
    tm = time.strptime(ts, '%Y-%m-%d_%H-%M-%S')
    return time.strftime('%Y-%m-%d %H:%M:%S', tm)


@website.route('/')
def get_index_html():
    global _USER_LINE_HTML, _INDEX_HTML, data_dir
    users_html = []
    for user_dir in Path(data_dir).iterdir():
        users_html.append(_USER_LINE_HTML.format(user_id=user_dir.name))
    index_html = _INDEX_HTML.format(users='\n'.join(users_html))
    return index_html


@website.route('/users/<user>')
def get_user_html(user):
    global _FILE_LINE_HTML, _USER_HTML, data_dir
    thoughts = []
    user_path = Path(data_dir) / user
    if not user_path.exists():
        return 404, ''
    for f in user_path.iterdir():
        ts = format_time_stamp(f.name[:-4])
        thought = f.read_text()
        thoughts.append(_FILE_LINE_HTML.format(time_stamp=ts, thought=thought))
    user_html = _USER_HTML.format(user=user, files='\n'.join(thoughts))
    return user_html


@click.argument('address')
@click.argument('data')
def run_webserver(address, data):
    global data_dir, website
    data_dir = data
    ip, port = address.split(':')
    website.run(host=ip, port=int(port), debug=False)
