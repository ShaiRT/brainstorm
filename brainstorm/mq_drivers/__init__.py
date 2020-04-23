"""A module for message queue drivers

Any Publisher or Consumer class in a 'driver_name_driver.py' file 
in this directory will be included in the module.
Files starting with '_' will be ignored.
The module imports as a dictionary of {'driver_name': {'publisher': Publiser, 'consumer': Consumer}}.

The Publisher class should have a publish(message) method,
and the Consumer class should have a consume(method)

# TODO: add support for publish and comsume methods
"""
import importlib
import inspect
import sys

from pathlib import Path


drivers = dict()
root = Path(inspect.getsourcefile(lambda: 0)).absolute().parent
for path in root.glob('**/*.py'):
    if path.name.startswith('_'):
        continue
    if not path.name.endswith('_driver.py'):
        continue
    sys.path.insert(0, str(path.parent))
    m = importlib.import_module(path.stem, package='brainstorm.mq_drivers')
    sys.path.pop(0)
    driver_name = path.name[:-10]
    drivers[driver_name] = dict()
    if 'Publisher' in m.__dict__ and inspect.isclass(m.__dict__['Publisher']):
        drivers[driver_name]['publisher'] = m.__dict__['Publisher']
    if 'Consumer' in m.__dict__ and inspect.isclass(m.__dict__['Consumer']):
        drivers[driver_name]['consumer'] = m.__dict__['Consumer']

sys.modules[__name__] = drivers
