from pathlib import Path
import importlib
import sys
import stringcase as sc
import json
import inspect


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
        if isinstance(obj, type):
            if not name.endswith('Parser'):
                continue
            parser_name = sc.snakecase(name)[:-7]
            parser = obj()
            parsers[parser_name] = parser.parse
            continue
        if callable(obj):
            if not name.startswith('parse_'):
                continue
            parsers[name[6:]] = obj


def parse(name, data):
    global parsers
    snapshot = json.loads(data)
    return json.dumps(parsers[name](snapshot))
