Automatic User Timezone Detection for Django
============================================

This app will auto-detect a user's timezone using JavaScript, 
then configure Django's timezone localization system 
accordingly. As a result, dates shown to users will 
be in their local timezones.

.. image:: https://badge.fury.io/py/django-tz-detect.png
    :target: https://badge.fury.io/py/django-tz-detect

.. image:: https://pypip.in/d/django-tz-detect/badge.png
    :target: https://pypi.python.org/pypi/django-tz-detect

How it works
------------

On the first page view you should find that tz_detect places a piece 
of asynchronous JavaScript code into your page using the template tag you inserted.
The script will obtain the user's GMT offset using ``getTimezoneOffset``, and post it 
back to Django. The offset is stored in the user's session and Django's timezone awareness is 
configured in the middleware.

The JavaScript will not be displayed in future requests.

Installation
------------

1. Either checkout tz_detect from GitHub, or install using pip:

.. code-block:: bash

    pip install django-tz-detect

2. Add ``tz_detect`` to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        'tz_detect',
    )

3. Update your ``urls.py`` file:

.. code-block:: python

    urlpatterns = patterns('',
        url(r'^tz-detect/', include('tz_detect.urls')),
        ...
    )

4. Add the detection template tag to your site, ideally in your base layout just before the ``</body>`` tag::
    
    {% load tz_detect %}
    {% tz_detect %}

5. Add ``TimezoneMiddleware`` to ``MIDDLEWARE_CLASSES``:

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        # Django defaults
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        # For tz_detect
        'tz_detect.middleware.TimezoneMiddleware',
     )

6. (Optional) Configure the countries in which your app will be most commonly used:

.. code-block:: python

    # These countries will be prioritized in the search
    # for a matching timezone. Consider putting your
    # app's most popular countries first.
    # Defaults to the top Internet using countries.
    TZ_DETECT_COUNTIRES = ('CN', 'US', 'IN', 'JP', 'BR', 'RU', 'DE', 'FR', 'GB')


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
