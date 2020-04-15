"""A module for snapshot parsers

Any ParserNameParser class or parse_parser_name(snapshot) function
in a '.py' file in this directory will be included in the module.
Files starting with '_' will be ignored.
The parser classes will have one instance created when imported, 
and must have a parse method.
"""
import importlib
import inspect
import json
import stringcase as sc
import sys

from pathlib import Path


parsers = dict()
root = Path(inspect.getsourcefile(lambda: 0)).absolute()
root = root.parent
for path in root.glob('**/*.py'):
    if path.name.startswith('_'):
        continue
    sys.path.insert(0, str(path.parent))
    m = importlib.import_module(path.stem, package='brainstorm.parsers')
    sys.path.pop(0)
    for name, obj in m.__dict__.items():
        if inspect.isclass(obj):
            if not name.endswith('Parser'):
                continue
            parser_name = sc.snakecase(name)[:-7]
            parser = obj()
            parsers[parser_name] = parser.parse
            continue
        if inspect.isfunction(obj):
            if not name.startswith('parse_'):
                continue
            parsers[name[6:]] = obj


def parse(name, data):
    """users parser to parse json snapshot data
    
    Args:
        name (str): the name of the parser to be used
        data (str): the snapshot data in json format
    
    Returns:
        str: the parsed data as json 
        if name is not an existing parser or 
        snapshot doesn't have a name field return None
    """
    global parsers
    if name not in parsers:
        return None
    snapshot = json.loads(data)
    if name not in snapshot:
        return None
    return json.dumps(parsers[name](snapshot))


def parse_path(name, path):
    """parse snapshot data in given path
    path has to be a file with data in json format
    
    Args:
        name (str): the name of the parser to be used
        path (str): the path of data to be parsed
    
    Returns:
        str: parsed information in json format
    """
    with open(path, 'rb') as f:
        data = f.read()
    return parse(name, data)


def _parse_and_publish(receiving_channel, method, properties,
                      data, *, host, port, parser):
    '''callback for message queue consuming
    '''
    parsed_data = parse(parser, data)
    if not parsed_data:
        receiving_channel.basic_ack(delivery_tag=method.delivery_tag)
        return
    params = pika.ConnectionParameters(host=host, port=port)
    connection = pika.BlockingConnection(params)
    publishing_channel = connection.channel()
    publishing_channel.exchange_declare(exchange='data', exchange_type='topic')
    publishing_channel.basic_publish(exchange='data',
                                     routing_key=parser, body=parsed_data)
    connection.close()
    receiving_channel.basic_ack(delivery_tag=method.delivery_tag)


def run_parser(name, url):
    """run parser to listen to message queue, parse data,
    and post back to 'data' topic exchange of the 
    message queue with routing_key=name.
    **supports rabbitmq as a message queue
    
    Args:
        name (str): name of the parser to be used
        url (str): url of the message queue
    """
    f = furl.furl(url)
    host = f.host
    port = f.port
    params = pika.ConnectionParameters(host=host, port=port)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange='snapshots', exchange_type='fanout')
    channel.queue_declare(queue=name)
    channel.queue_bind(exchange='snapshots', queue=name)
    channel.basic_qos(prefetch_count=1)
    callback = ft.partial(_parse_and_publish, host=host, port=port, parser=name)
    channel.basic_consume(queue=name, on_message_callback=callback)
    channel.start_consuming()
