#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'PyYAML'
]

setup(
    name='beet_playlist',
    version='0.0.1',
    description="Playlist manager for beet",
    long_description=readme + '\n\n' + history,
    author="Ignacio Rossi",
    author_email='rossi.ignacio@gmail.com ',
    url='https://github.com/pignacio/beet_playlist',
    packages=[
        'beet_playlist',
    ],
    package_dir={'beet_playlist':
                 'beet_playlist'},
    include_package_data=True,
    install_requires=requirements,
    license='GPLv3',
    zip_safe=False,
    keywords='beets beet playlist',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
)
