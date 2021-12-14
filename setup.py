from io import open

from setuptools import find_packages, setup

with open('crawlio/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.strip().split('=')[1].strip(' \'"')
            break
    else:
        version = '0.0.1'

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

REQUIRES = []

kwargs = {
    'name': 'crawlio',
    'version': version,
    'description': "Simple and customizable web crawler built with Python's asyncio",
    'long_description': readme,
    'long_description_content_type': "text/markdown",
    'author': 'Maximilian Wolf',
    'author_email': 'maximilian.wolf@innovinati.com',
    'url': 'https://github.com/maximiliancw/crawlio',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Framework :: AsyncIO'
    ],
    'install_requires': REQUIRES,
    'tests_require': ['coverage', 'pytest'],
    'packages': find_packages(exclude=('tests', 'tests.*')),

}

setup(**kwargs)
