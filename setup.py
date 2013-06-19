#!/usr/bin/env python

from os.path import exists
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from django_tz_detect import __version__

setup(
    name='django-tz-detect',
    version=__version__,
    # Your name & email here
    author='',
    author_email='',
    # If you had django_tz_detect.tests, you would also include that in this list
    packages=['django_tz_detect'],
    # Any executable scripts, typically in 'bin'. E.g 'bin/do-something.py'
    scripts=[],
    # REQUIRED: Your project's URL
    url='',
    # Put your license here. See LICENSE.txt for more information
    license='',
    # Put a nice one-liner description here
    description='',
    long_description=open('README.rst').read() if exists("README.rst") else "",
    # Any requirements here, e.g. "Django >= 1.1.1"
    install_requires=[
        "django>=1.4"
    ],
)
