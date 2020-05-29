from setuptools import find_packages
from setuptools import setup


setup(
    name = 'brainstorm',
    version = '0.1.0',
    author = 'Shai Rahat',
    description = 'Brain computer interface.',
    packages = find_packages(),
    install_requires = ['click', 
                        'flask', 
                        'Pillow', 
                        'blessings', 
                        'Flask-Cors', 
                        'furl', 
                        'matplotlib',
                        'numpy',
                        'pika',
                        'prettytable-extras',
                        'protobuf',
                        'pymongo',
                        'requests',
                        'stringcase'],
    tests_require = ['pytest', 'pytest-cov', 'requests-mock'],
)
