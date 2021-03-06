#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup  # noqa, analysis:ignore
except ImportError:
    print ('''please install setuptools
python -m pip install setuptools
or
python -m pip install setuptools''')
    raise ImportError()

from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

## Setup

setup(
    name='DicksonUI-Micro',
    version='2.0.0',
    author='Kavindu Santhusa',
    author_email='kavindusanthusa@gmail.com',
    license='MIT',
    url='https://github.com/Ksengine/DicksonUI',
    download_url='https://pypi.python.org/pypi/DicksonUI',
    keywords='''python, gui, html, css, js, javascript, ui, servelight, server, 
user-interface, graphical-user-interface, lightweight, full-featured, 
browser, browser-based, webview, html, view, remote, interface'''
        ,
    description='Lightweight And Full Featured Browser Based UI / GUI (Graphical User Interface Library)'
        ,
    long_description=long_description,
    long_description_content_type='text/markdown',
    platforms='any',
    packages=["dicksonui"],
    zip_safe=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
        ],
    include_package_data=True,
    )
