import blessings
import click
import sys
import traceback

from .saver import save_from_path, run_saver


@click.group()
def saver_cli():
    pass


@saver_cli.command('save')
@click.option('database_url', '-d', '--database',
              default='mongodb://localhost:27017/',
              show_default=True, help='the url of the database')
@click.argument('path')
def cli_save_from_path(database_url, path):
    '''Save data in given path to database in given url
    '''
    save_from_path(database_url, path)


@click.option('tb', '-t', '--traceback', is_flag=True,
              default=False, show_default=True,
              help='show full traceback on failure')
@saver_cli.command('run-saver')
@click.argument('database_url')
@click.argument('mq_url')
def cli_run_saver(database_url, mq_url, tb=False):
    """Run the saver to save messages from message queue in given url to database.
    The saver saves all messages received in 'data' topic exchange.
    """
    try:
        run_saver(database_url, mq_url)
    except Exception as e:
        track = traceback.format_exc()
        t = blessings.Terminal()
        if tb:
            click.echo(t.red(track))
        else:
            click.echo(t.red(
                f'Failed with exception {type(e).__name__}: \n{e}'))
        sys.exit(1)


if __name__ == '__main__':
    saver_cli()
