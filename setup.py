import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

from tz_detect import __version__

setup(
    name='django-tz-detect',
    version=__version__,
    packages=find_packages(exclude=['example']),
    include_package_data=True,
    license='MIT License',
    description='Automatic user timezone detection for django',
    long_description=README,
    url='http://github.com/adamcharnock/django-tz-detect',
    author='Adam Charnock',
    author_email='adam@adamcharnock.com',
    install_requires=[
        'django>=1.4',
        'pytz',
    ],    
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    zip_safe=False,
)
