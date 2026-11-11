django-tz-detect
================

.. image:: https://badge.fury.io/py/django-tz-detect.svg
    :target: https://badge.fury.io/py/django-tz-detect

.. image:: https://img.shields.io/pypi/pyversions/django-tz-detect.svg
    :target: https://pypi.python.org/pypi/django-tz-detect/

.. image:: https://img.shields.io/pypi/djversions/django-tz-detect.svg
    :target: https://pypi.python.org/pypi/django-tz-detect/

.. image:: https://github.com/adamcharnock/django-tz-detect/actions/workflows/test.yml/badge.svg
    :target: https://github.com/adamcharnock/django-tz-detect/actions/workflows/test.yml

This app will auto-detect a user's timezone using JavaScript, then
configure Django's timezone localization system accordingly. As a
result, dates shown to users will be in their local timezones.

Maintained by `Basil Shubin <https://github.com/bashu/>`_, and some great
`contributors <https://github.com/bashu/django-tz-detect/contributors>`_.

How it works
------------

On the first page view you should find that ``tz_detect`` places a
piece of asynchronous JavaScript code into your page using the
template tag you inserted. The script reads the browser's timezone
name (such as ``Europe/Amsterdam``) using
``Intl.DateTimeFormat().resolvedOptions().timeZone``, along with the
UTC offset from ``getTimezoneOffset``, and posts both back to Django.

The timezone name is stored in the user's session. If the server doesn't
recognise the name, the offset is stored instead, and the middleware
picks the closest matching timezone (see ``TZ_DETECT_COUNTRIES`` below).
On each request, the middleware activates the stored timezone in
Django's timezone support.

The JavaScript will not be displayed in future requests. If the stored
timezone becomes unusable, it is dropped from the session and detected
again on the next page view.

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

       MIDDLEWARE += (
           'tz_detect.middleware.TimezoneMiddleware',
       )

7. (Optional) Configure optional settings

   Set the countries in which your app will be most commonly used:

   .. code-block:: python

       # These countries will be prioritized in the search
       # for a matching timezone. Consider putting your
       # app's most popular countries first.
       # Defaults to the top Internet using countries.
       TZ_DETECT_COUNTRIES = ('CN', 'US', 'IN', 'JP', 'BR', 'RU', 'DE', 'FR', 'GB')

   Set the session key that will be used to store the detected timezone

   .. code-block:: python

       # Session key to use, defaults to "detected_tz"
       TZ_SESSION_KEY = "my-session-key"

Please see ``example`` application. This application is used to manually
test the functionalities of this package. This also serves as a good
example.

Requires Python 3.11+ and Django 5.2+.

Caveats
-------

- Django's timezone awareness will not be available on the first page view
- This method requires JavaScript
- Timezone detection uses the browser's timezone setting (its timezone name, or the UTC offset as a fallback), not the user's location

Future expansion
----------------

- A hook to allow the timezone to be stored against a user
- Allow timezones to be manually specified
- Improve timezone detection
- Optionally using HTML5's location API for better timezone determination

Contributing
------------

If you've found a bug, implemented a feature or customized the template and
think it is useful then please consider contributing. Patches, pull requests or
just suggestions are welcome!

Credits
-------

`django-tz-detect <https://github.com/bashu/django-tz-detect/>`_ was originally started by `Adam Charnock <https://adamcharnock.com/>`_ who has now unfortunately abandoned the project.

License
-------

``django-tz-detect`` is released under the MIT license.
