SECRET_KEY = "DUMMY_SECRET_KEY"  # noqa: S105

# Application definition

PROJECT_APPS = ["tz_detect.tests", "tz_detect"]


INSTALLED_APPS = [
    "django.contrib.sites",
    "django.contrib.sessions",
    "django.contrib.contenttypes",
    *PROJECT_APPS,
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "tz_detect.middleware.TimezoneMiddleware",
]

SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

USE_TZ = True
