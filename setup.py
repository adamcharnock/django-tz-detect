#!/usr/bin/env python

from os.path import exists
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from tz_detect import __version__

setup(
    name='django-tz-detect',
    version=__version__,
    author='Adam Charnock',
    author_email='adam@adamcharnock.com',
    packages=['tz_detect'],
    package_data={
        'tz_detect': [
            'templates/tz_detect/detector.html',
            'static/tz_detect/js/tzdetect.js',
            'static/tz_detect/js/tzdetect.min.js',
        ]
    },
    # Any executable scripts, typically in 'bin'. E.g 'bin/do-something.py'
    scripts=[],
    # REQUIRED: Your project's URL
    url='https://github.com/adamcharnock/django-tz-detect',
    license='MIT',
    description='Automatic user timezone detection for django',
    long_description=open('README.rst').read() if exists("README.rst") else "",
    # Any requirements here, e.g. "Django >= 1.1.1"
    install_requires=[
        'django>=1.4',
        'pytz',
    ],
)
