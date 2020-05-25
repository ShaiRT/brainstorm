def parse_feelings(snapshot):
    '''return only the snapshot feelings
    **assumes snapshot has feelings, a user and datetime

    Args:
        snapshot (dict): snapshot with feelings

    Returns:
        dict -- feelings information
    '''
    parsed_info = dict()
    parsed_info['user'] = snapshot['user']
    parsed_info['datetime'] = snapshot['datetime']
    parsed_info['feelings'] = snapshot['feelings']
    return parsed_info
