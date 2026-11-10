Changes
-------

0.6.1 (2026-11-10)
~~~~~~~~~~~~~~~~~~

* Fixed ``LoginRequiredMiddleware`` (Django 5.1+) redirecting anonymous
  visitors' timezone requests to the login page, #79.

0.6.0 (2026-11-10)
~~~~~~~~~~~~~~~~~~

* Now requires Python 3.11+ and Django 5.2+.
* Migrated packaging to ``pyproject.toml``, and added pre-commit hooks and
  GitHub Actions CI/release workflows.
* Made the session key configurable with the ``TZ_SESSION_KEY`` setting, #71.
* Fixed timezone names containing ``+`` (such as ``Etc/GMT+3``) being sent
  to the server as ``Etc/GMT 3``, #70, #75.
* Fixed an invalid or unknown timezone in the session raising
  ``UnknownTimeZoneError`` on every request, #70, #76.
* Replaced ``pytz`` with Python's ``zoneinfo``, and dropped the ``pytz``
  dependency. On Django 5+, ``pytz`` zones shifted every datetime saved
  through forms by the zone's LMT offset (e.g. ``-07:53`` instead of
  ``-07:00`` for ``America/Los_Angeles``), #73, #80.

0.5.0
~~~~~

* Prefer Intl timezone over offset, #63

0.4.0
~~~~~

* Support Django 2.2, 3.0, 3.1, 3.2, 4.0
* Support Python 3.7, 3.8, 3.9, 3.10
* Drop Python 2 support
* Switch from Travis CI to GitHub Actions

0.3.0 (2019-11-26)
~~~~~~~~~~~~~~~~~~

* Set attributes on script tag. (Craig Anderson)

0.2.10 (2019-03-30)
~~~~~~~~~~~~~~~~~~~

* Dropped support for django < 1.11 (Basil Shubin)
* Template library load: staticfiles is deprecated in favor of static (Pi Delport)
* MIDDLEWARE_CLASSES renamed to MIDDLEWARE in Django 1.10 (Craig Anderson)
* Add Tox configuration (Pi Delport)
* Simplify offset_to_timezone implementation to use min() (Pi Delport)
* Update offset_to_timezone to handle edge cases more accurately (Pi Delport)
* Add tests for all hourly UTC offsets, with known mis-detections (Pi Delport)

0.2.9 (2017-12-18)
~~~~~~~~~~~~~~~~~~

* Excluding testing of django 2.0 on python 2.7 (Adam Charnock)
* Adding django 2.0 to build matrix (Adam Charnock)
* Implement handle of settings.CSRF_HEADER_NAME (Roman Gorbil)
* upgraded test suite (Basil Shubin)
* Travis config: Add Django 1.11, exclude Python 2.7/Django master (because
  Django 2.0 will not support Python 2.7), and allow tests against Django
  master to fail (Drew Hubl)
* fixed typo, close #31 (Basil Shubin)

0.2.8 (2016-10-21)
~~~~~~~~~~~~~~~~~~

* dropped support for python 2.6 & 3.3 (bashu)
* make sure example project runs under django 1.10.x (bashu)
* Update README.rst (bashu)
* Update .travis.yml (Eric Wang)
* Add Django 1.10 support (Eric Wang)

0.2.7 (2016-04-28)
~~~~~~~~~~~~~~~~~~

* added missing VERSION file (bashu)
* Renaming CHANGES -> CHANGES.txt (as required by seed) (bashu)
* Updating version to be stored in VERSION file (as now done by seed) (bashu)
* Clean up imports (Filip Figiel)
* Don't expect request in templatetag context. Fixes #26 (Filip Figiel)

0.2.6 (2016-02-13)
~~~~~~~~~~~~~~~~~~

* fix for Django 1.10 (kudos to @PetrDlouhy)
* Added django 1.9 support (Basil Shubin)

0.2.5 (2015-05-06)
~~~~~~~~~~~~~~~~~~

* python 3 support (Basil Shubin)

0.2.4 (2015-05-06)
~~~~~~~~~~~~~~~~~~

* Handle existing sessions storing ``basestring`` objects (Basil Shubin)

0.2.3 (2015-05-24)
~~~~~~~~~~~~~~~~~~

* Correctly handle NonExistentTimeError exception. (Basil Shubin)
* Support django 1.6+ default session serializer, JSONSerializer (Doug Cox)
* Backward compatibility with django 1.4 (Basil Shubin)

0.2.2 (2013-08-31)
~~~~~~~~~~~~~~~~~~

* Fixing typo in setting name. Thanks to @ustun for noticing. (Adam Charnock)

0.2.1 (2013-08-30)
~~~~~~~~~~~~~~~~~~

* Updating setup.py to use setuptools exclusively (as per recent seed changes) (Adam Charnock)

0.2.0 (2013-08-30)
~~~~~~~~~~~~~~~~~~

* Correcting JS error (for issue #2) (Adam Charnock)
* Work on issue #2 - Disable posting timezone to server if cookies are disabled (Adam Charnock)
* Adding badges to readme (Adam Charnock)

0.1.5 (2013-06-26)
~~~~~~~~~~~~~~~~~~

* updating manifest (Adam Charnock)
* remove offending line (Rich Atkinson)
* insert new script next to another script, not just inside opening <html> (Rich Atkinson)

0.1.4 (2013-06-19)
~~~~~~~~~~~~~~~~~~

* Fixing setup.py packages directive (Adam Charnock)

0.1.3 (2013-06-19)
~~~~~~~~~~~~~~~~~~

* Fixing setup.py packages directive (Adam Charnock)

0.1.2 (2013-06-19)
~~~~~~~~~~~~~~~~~~

* Fixing setup.py packages directive (Adam Charnock)

0.1.1 (2013-06-19)
~~~~~~~~~~~~~~~~~~

* Fixing setup.py packages directive (Adam Charnock)

0.1.0 (2013-06-19)
~~~~~~~~~~~~~~~~~~

* First version
