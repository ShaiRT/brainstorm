from brainstorm.utils.protobuf_driver import ProtobufDriver


class Reader:

    def __init__(self, path, driver_class=ProtobufDriver):
        self.driver = driver_class(path)
        self.user = self.driver.get_user()

    def __getattr__(self, attr):
        if attr in ['user_id', 'username', 'birthday', 'gender']:
            return self.user[attr]

    def __iter__(self):
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


def read(path):
    reader = Reader(path)
    print(reader)
    for snapshot in reader:
        date = snapshot['datetime'].strftime('%B%e, %Y')
        time = snapshot['datetime'].strftime('%H:%M:%S.%f')
        print(f'Snapshot from {date} at {time}')
