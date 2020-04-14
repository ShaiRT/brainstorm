"""A client that sends snapshots to a server
"""
import bson
import furl
import requests

import brainstorm.client.reader as reader


def upload_sample(path, host='127.0.0.1', port=8000, reader_driver='protobuf'):
    '''Upload a sample in given path to the server
    The snapshots are POSTed to http://host:port/snapshot in bson format

    Arguments:
        path {str} -- the path of the sample file

    Keyword Arguments:
        host {str} -- ip address of the server (default: {'127.0.0.1'})
        port {number} -- the server port (default: {8000})
        reader_driver {str} -- a driver for the sample reader
                               (from brainstorm.reader_drivers)
                               (default: {'protobuf'})

    Raises:
        ConnectionError -- when communication to the server fails
    '''
    my_reader = reader.Reader(path, driver=reader_driver)
    for snapshot in my_reader:
        snapshot['user'] = my_reader.user
        url = furl.furl(scheme='http', host=host,
                        port=port, path='snapshot').url
        r = requests.post(url=url, data=bson.encode(snapshot),
                          headers={'Connection': 'close'})
        if not r.status_code == 200:
            raise ConnectionError(f'Upload failed \
                with status code: {r.status_code}')
        r.close()
