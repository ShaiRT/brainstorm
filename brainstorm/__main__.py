from .server import run_server
from .client import upload_thought
from .web import run_webserver
from .utils import read
from .client import run_client

import click

@click.group()
def cli():
    pass

@cli.group()
def server():
	pass

@cli.group()
def client():
	pass

run_webserver = cli.command()(run_webserver)
run_server = server.command('run')(run_server)
read = cli.command()(read)
upload_thought = client.command()(upload_thought)
run_client = client.command('run')(run_client)


cli()
