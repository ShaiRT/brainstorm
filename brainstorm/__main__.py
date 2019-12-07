from .server import run_server
from .client import upload_thought
from .web import run_webserver
import click


@click.group()
def cli():
    pass


run_webserver = cli.command()(run_webserver)
upload_thought = cli.command()(upload_thought)
run_server = cli.command()(run_server)

cli()
