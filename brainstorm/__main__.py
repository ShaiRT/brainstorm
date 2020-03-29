from .server import run_server
from .client import upload_sample
from .web import run_webserver
import click
from . import parsers


@click.group()
def cli():
    pass

run_webserver = cli.command()(run_webserver)

cli()
