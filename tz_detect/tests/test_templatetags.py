from datetime import datetime

import pytz
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.timezone import activate, get_current_timezone_name

from tz_detect.middleware import TimezoneMiddleware
from tz_detect.templatetags.tz_detect import tz_detect
from tz_detect.utils import convert_header_name, offset_to_timezone
from tz_detect.defaults import TZ_SESSION_KEY
from tz_detect.views import SetOffsetView


class TemplatetagTestCase(TestCase):
    def test_no_request_context(self):
        try:
            tz_detect({})
        except KeyError as e:
            if e.message == "request":
                self.fail("Templatetag shouldn't expect request in context.")
            else:
                raise
