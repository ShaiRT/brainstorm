"""A sample reader
Uses the drivers in brainstorm.reader_drivers

The driver provided to the reader must implement the following interface:
a get_user() method that returns a user as a dict.
a get_snapshot() method that returns a snapshot as a dict.
**the driver may assume that get_user() will be called before get_snapshot()
"""
import brainstorm.reader_drivers as drivers
import click


class Reader:

    """
    Attributes:
        user (dict): the user from the sample
        user_id (int)
        username (str)
        birthday (datetime.datetime)
        gender (str)
    """
    
    def __init__(self, path, *, driver='protobuf'):
        '''
        Arguments:
            path {str} -- a path to a sample in the format of the driver
        
        Keyword Arguments:
            driver {str} -- the name of the driver for the sample (default: {'protobuf'})
                            must be a driver from brainstorm.reader_drivers 
        '''
        self.driver = drivers[driver](path)
        self.user = self.driver.get_user()

    def __getattr__(self, attr):
        if attr in ['user_id', 'username', 'birthday', 'gender']:
            return self.user[attr]

    def __iter__(self):
        """
        Yields:
            dict: snapshots from the sapmle
        """
        while(True):
            snapshot = self.driver.get_snapshot()
            if snapshot is None:
                break
            yield snapshot

    def __repr__(self):
        rep = f'user {self.user_id}: {self.username}, '
        birthday = self.birthday.strftime('%B%e, %Y')
        rep += f'born {birthday} '
        rep += f'({self.gender})'
        return rep


@click.group()
def reader_cli():
    pass


@reader_cli.command()
@click.option('driver', '-d', '--driver', default='protobuf', show_default=True)
@click.argument('path')
def read(path, driver='protobuf'):
    '''Read the sample in path and print the information
    
    Arguments:
        path {str} -- a path to a sample
    
    Keyword Arguments:
        driver {str} -- the name of the driver for the sample (default: {'protobuf'})
                        must be a driver from brainstorm.reader_drivers
    '''
    reader = Reader(path, driver=driver)
    print(reader)
    for snapshot in reader:
        date = snapshot['datetime'].strftime('%B%e, %Y')
        time = snapshot['datetime'].strftime('%H:%M:%S.%f')
        print(f'Snapshot from {date} at {time}')


if __name__ == '__main__':
    reader_cli()
