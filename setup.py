#!/usr/bin/env python

import os
import re
import sys
import codecs
import subprocess

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class TestRunner(TestCommand):
    user_options = []

    def run(self):
        raise SystemExit(subprocess.call([sys.executable, 'runtests.py']))


def read(*parts):
    file_path = os.path.join(os.path.dirname(__file__), *parts)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='django-tz-detect',
    version=read('VERSION'),
    license='MIT License',

    install_requires=[
        'django>=1.4.2',
        'pytz',
        'six',
    ],    
    requires=[
        'Django (>=1.4.2)',
    ],
    
    description='Automatic user timezone detection for django',
    long_description=read('README.rst'),

    author='Adam Charnock',
    author_email='adam@adamcharnock.com',

    maintainer='Basil Shubin',
    maintainer_email='basil.shubin@gmail.com',

    url='http://github.com/adamcharnock/django-tz-detect',
    download_url='https://github.com/adamcharnock/django-tz-detect/zipball/master',

    packages=find_packages(exclude=('example*', '*.tests*')),
    include_package_data=True,

    tests_require=[
    ],
    cmdclass={
        'test': TestRunner,
    },
    
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
