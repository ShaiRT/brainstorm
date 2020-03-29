def parse_feelings(snapshot):
    parsed_info = dict()
    parsed_info['user'] = snapshot['user']
    parsed_info['datetime'] = snapshot['datetime']
    parsed_info['feelings'] = snapshot['feelings']
    return parsed_info
