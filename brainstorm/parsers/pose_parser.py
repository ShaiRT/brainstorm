def parse_pose(snapshot):
    parsed_info = dict()
    parsed_info['user'] = snapshot['user']
    parsed_info['datetime'] = snapshot['datetime']
    parsed_info['pose'] = snapshot['pose']
    return parsed_info
