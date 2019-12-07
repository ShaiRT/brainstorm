from setuptools import setup, find_packages


setup(
    name = 'brainstorm',
    version = '0.1.0',
    author = 'Shai Rahat',
    description = 'Brain computer interface.',
    packages = find_packages(),
    install_requires = ['click', 'flask'],
    tests_require = ['pytest', 'pytest-cov'],
)
