django-tz-detect
================

.. image:: https://img.shields.io/pypi/v/django-tz-detect.svg
    :target: https://pypi.python.org/pypi/django-tz-detect/

.. image:: https://img.shields.io/pypi/dm/django-tz-detect.svg
    :target: https://pypi.python.org/pypi/django-tz-detect/

.. image:: https://img.shields.io/github/license/adamcharnock/django-tz-detect.svg
    :target: https://pypi.python.org/pypi/django-tz-detect/

.. image:: https://coveralls.io/repos/adamcharnock/django-tz-detect/badge.svg?branch=develop
    :target: https://coveralls.io/r/adamcharnock/django-tz-detect?branch=develop

This app will auto-detect a user's timezone using JavaScript, then
configure Django's timezone localization system accordingly. As a
result, dates shown to users will be in their local timezones.

Authored by `Adam Charnock <https://adamcharnock.com/>`_, and some great `contributors <https://github.com/adamcharnock/django-tz-detect/contributors>`_.

How it works
------------

On the first page view you should find that ``tz_detect`` places a
piece of asynchronous JavaScript code into your page using the
template tag you inserted.  The script will obtain the user's GMT
offset using ``getTimezoneOffset``, and post it back to Django. The
offset is stored in the user's session and Django's timezone awareness
is configured in the middleware.

The JavaScript will not be displayed in future requests.

Installation
------------

1. Either checkout ``tz_detect`` from GitHub, or install using pip:

   .. code-block:: bash

       pip install django-tz-detect

2. Add ``tz_detect`` to your ``INSTALLED_APPS``:

   .. code-block:: python

       INSTALLED_APPS += (
           'tz_detect',
       )

3. Be sure you have the ``django.template.context_processors.request`` processor
   
   .. code-block:: python

       TEMPLATES = [
           {
               ...
               'OPTIONS': {
                   'context_processors': [
                       ...
                       'django.template.context_processors.request',
                   ],
               },
           },
       ]

4. Update your ``urls.py`` file:

   .. code-block:: python

       urlpatterns += [
           path('tz_detect/', include('tz_detect.urls')),
       ]

5. Add the detection template tag to your site, ideally in your base layout just before the ``</body>`` tag:

   .. code-block:: html+django

       {% load tz_detect %}
       {% tz_detect %}

6. Add ``TimezoneMiddleware`` to ``MIDDLEWARE``:

   .. code-block:: python

       import django

       MIDDLEWARE += (
           'tz_detect.middleware.TimezoneMiddleware',
       )

       if django.VERSION < (1, 10):
           MIDDLEWARE_CLASSES += (
               'tz_detect.middleware.TimezoneMiddleware',
           )

7. (Optional) Configure the countries in which your app will be most commonly used:

   .. code-block:: python

       # These countries will be prioritized in the search
       # for a matching timezone. Consider putting your
       # app's most popular countries first.
       # Defaults to the top Internet using countries.
       TZ_DETECT_COUNTRIES = ('CN', 'US', 'IN', 'JP', 'BR', 'RU', 'DE', 'FR', 'GB')

Please see ``example`` application. This application is used to manually
test the functionalities of this package. This also serves as a good
example.

You need only Django 1.8 or above to run that. It might run on older
versions but that is not tested.

Caveats
-------

- Django's timezone awareness will not be available on the first page view
- This method requires JavaScript
- Timezone detection is done entirely from the user's GMT offset, not from their location

Future expansion
----------------

- A hook to allow the timezone to be stored against a user
- Allow timezones to be manually specified
- Improve timezone detection
- Optionally using HTML5's location API for better timezone determination
