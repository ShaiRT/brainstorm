"""A sample reader.
Uses the drivers in brainstorm.client.reader_drivers

The driver provided to the reader must implement the following interface:
a get_user() method that returns a user as a dict.
a get_snapshot() method that returns a snapshot as a dict.
**the driver may assume that get_user() will be called before get_snapshot()
"""
from . import reader_drivers as drivers


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
            path (str): a path to a sample in the format of the driver

        Keyword Arguments:
            driver (str): the name of the driver for the sample
                          (default: {'protobuf'})
                          must be a driver from brainstorm.reader_drivers
        '''
        if driver not in drivers:
            raise NotImplementedError(f"No reader driver named '{driver}'")
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
