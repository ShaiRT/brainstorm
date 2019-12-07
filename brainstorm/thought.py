import struct
import datetime as dt


class Thought:
    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        user_id, timestamp, thought = \
            self.user_id, self.timestamp, self.thought
        cls = self.__class__.__name__
        return f'{cls}({user_id=}, {timestamp=!r}, {thought=!r})'

    def __str__(self):
        timestamp_str = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        return f'[{timestamp_str}] user {self.user_id}: {self.thought}'

    def __eq__(self, other):
        if not isinstance(other, Thought):
            return NotImplemented
        if not self.user_id == other.user_id:
            return False
        if not self.timestamp == other.timestamp:
            return False
        return self.thought == other.thought

    def serialize(self):
        encoded_thought = self.thought.encode('utf-8')
        time_int = int(dt.datetime.timestamp(self.timestamp))
        data = struct.pack('QQI', self.user_id, time_int, len(encoded_thought))
        data += encoded_thought
        return data
    
    def deserialize(data):
        user_id, timestamp, thought_size = struct.unpack('QQI', data[:20])
        thought = data[20:].decode('utf-8')
        timestamp = dt.datetime.fromtimestamp(timestamp)
        return Thought(user_id, timestamp, thought)
