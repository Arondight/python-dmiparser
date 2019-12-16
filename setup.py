#!/usr/bin/env python3

from setuptools import setup, find_packages

project = 'dmiparser'
version = '0.1'
description = 'This parse dmidecode output to JSON'
long_description = description
url = 'https://github.com/Arondight/python-dmiparser'

setup(
    name                    = project,
    version                 = version,
    description             = description,
    long_description        = long_description,
    author                  = 'Qin Fandong',
    author_email            = 'shell_way@foxmail.com',
    url                     = url,
    download_url            = "%s/releases" %(url),
    classifiers             = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    platforms               = ['Any'],
    install_requires        = [
        'setuptools'
        'wheel'
    ],
    packages                = find_packages(),
    include_package_data    = True,
)

