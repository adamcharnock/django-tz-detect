"""
Django settings for the django-tz-detect example project.

For more information on this file, see
https://docs.djangoproject.com/en/stable/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/stable/ref/settings/
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "YOUR_SECRET_KEY"  # noqa: S105

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

PROJECT_APPS = [
    "tz_detect",
]

INSTALLED_APPS = [
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    *PROJECT_APPS,
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "tz_detect.middleware.TimezoneMiddleware",
]

ROOT_URLCONF = "example.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.i18n",
                "django.template.context_processors.request",
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

# Keep sessions in signed cookies, so the in-memory database needs no migrations.
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/

TIME_ZONE = "UTC"

# django-tz-detect: reload the first page once the timezone is detected.
TZ_DETECT_RELOAD = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/

STATIC_URL = "static/"
