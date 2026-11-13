Example
=======

A minimal Django project for trying out ``django-tz-detect`` by hand.

Run it from the repository root with `uv <https://docs.astral.sh/uv/>`_:

.. code-block:: bash

    uv run python -m example.manage runserver

Then open http://127.0.0.1:8000/. After the first page view the detected
timezone is stored in the session, and the page reloads once to show the
time in it.
