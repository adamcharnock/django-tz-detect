import os

SECRET_KEY = "h_ekayhzss(0lzsacd5cat7d=pu#51sh3w&uqn&#3#tz26vuq4"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

INSTALLED_APPS = [
    "django.contrib.sites",
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    "tz_detect",
]

MIDDLEWARE_CLASSES = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "tz_detect.middleware.TimezoneMiddleware",
]

MIDDLEWARE = MIDDLEWARE_CLASSES

SITE_ID = 1
