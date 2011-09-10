#!/usr/bin/env python

from setuptools import setup

setup(
    name='pyspotify-ctypes',
    version='0.1',
    description='Ctypes-based Spotify bindings for python',
    author='Mikel Azkolain',
    author_email='azkotoki@gmail.com',
    url='http://forge.azkotoki.org/pyspotify-ctypes',
    package_dir = {'': 'src'},
    packages=['_spotify', 'spotify'],
    zip_safe=False,
)
