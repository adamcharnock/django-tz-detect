#!/usr/bin/env python

import codecs
import os
import re
import subprocess
import sys

from setuptools import find_packages, setup


def read(*parts):
    file_path = os.path.join(os.path.dirname(__file__), *parts)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="django-tz-detect",
    version=read("VERSION").strip(),
    license="MIT License",
    install_requires=[
        "django>=2.2",
        "pytz",
    ],
    description="Automatic user timezone detection for django",
    long_description=read("README.rst"),
    author="Adam Charnock",
    author_email="adam@adamcharnock.com",
    maintainer="Basil Shubin",
    maintainer_email="basil.shubin@gmail.com",
    url="http://github.com/adamcharnock/django-tz-detect",
    download_url="https://github.com/adamcharnock/django-tz-detect/zipball/master",
    packages=find_packages(exclude=("example*", "*.tests*")),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
