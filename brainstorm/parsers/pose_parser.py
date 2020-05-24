def parse_pose(snapshot):
    '''return only the snapshot pose
    **assumes snapshot has pose, a user and datetime
    
    Args:
        snapshot (dict): snapshot with pose
    
    Returns:
        dict -- pose information
    '''
    parsed_info = dict()
    parsed_info['user'] = snapshot['user']
    parsed_info['datetime'] = snapshot['datetime']
    parsed_info['pose'] = snapshot['pose']
    return parsed_info
