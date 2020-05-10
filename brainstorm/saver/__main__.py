import brainstorm.database_drivers as db_drivers
import brainstorm.mq_drivers as mq_drivers
import click
import datetime as dt
import furl
import json

from brainstorm.saver.saver import save_from_path, run_saver


@click.group()
def saver_cli():
    pass


@saver_cli.command('save')
@click.option('database_url', '-d', '--database',
              default='mongodb://localhost:27017/', show_default=True, help='the url of the database')
@click.argument('path')
def cli_save_from_path(database_url, path):
    '''Save data in given path to database in given url
    '''
    save_from_path(database_url, path)


@saver_cli.command('run-saver')
@click.argument('database_url')
@click.argument('mq_url')
def cli_run_saver(database_url, mq_url):
    """Run the saver to save messages from message queue in given url to database.
    The saver saves all messages received in 'data' topic exchange.
    """
    run_saver(database_url, mq_url)


if __name__ == '__main__':
    saver_cli()
