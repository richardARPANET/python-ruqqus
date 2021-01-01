#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
from codecs import open

from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

with open('README.md', 'r', encoding='utf-8') as rm_file:
    readme = rm_file.read()

with open('HISTORY.md', 'r', encoding='utf-8') as hist_file:
    history = hist_file.read()

setup(
    name='ruqqus',
    version='1.0.0.dev0',
    author='Ruqqus LLC',
    author_email='info@ruqqus.com',
    description='Ruqqus API Wrapper',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    url='https://github.com/ruqqus/python-ruqqus',
    packages=find_packages(exclude=['tests*']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
