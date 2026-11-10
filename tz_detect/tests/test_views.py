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


class ViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def add_session(self, request):
        get_response = lambda x: HttpResponse("")
        SessionMiddleware(get_response).process_request(request)

    def test_xhr_valid_offset(self):
        request = self.factory.post("/abc", {"offset": "-60"})
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(TZ_SESSION_KEY, request.session)
        self.assertIsInstance(request.session[TZ_SESSION_KEY], int)

    def test_xhr_valid_timezone(self):
        timezone_name = "Europe/Amsterdam"
        request = self.factory.post("/abc", {"timezone": timezone_name})
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(TZ_SESSION_KEY, request.session)
        self.assertEqual(request.session[TZ_SESSION_KEY], timezone_name)

    def test_xhr_invalid_timezone_fallback(self):
        timezone_name = "Etc/GMT 3"
        request = self.factory.post("/abc", {"timezone": timezone_name, "offset": "-180"})
        self.add_session(request)
        response = SetOffsetView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn(TZ_SESSION_KEY, request.session)
        self.assertEqual(request.session[TZ_SESSION_KEY], -180)

    def test_xhr_bad_method(self):
        request = self.factory.get("/abc")
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        self.assertEqual(response.status_code, 405)

    def test_xhr_no_offset(self):
        request = self.factory.post("/abc")
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_xhr_bad_offset(self):
        request = self.factory.post("/abc", {"offset": "12foo34"})
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_middleware_timezone_string(self):
        timezone_name = "Europe/Amsterdam"
        request = self.factory.post("/abc", {"timezone": timezone_name})
        self.add_session(request)
        request.session[TZ_SESSION_KEY] = timezone_name

        get_response = lambda x: HttpResponse("")
        TimezoneMiddleware(get_response).process_request(request)
        tz_name = get_current_timezone_name()
        self.assertEqual(tz_name, timezone_name)

    def test_middleware_invalid_timezone_string(self):
        timezone_name = "Etc/GMT 3"
        request = self.factory.post("/abc", {"timezone": timezone_name})
        self.add_session(request)
        request.session[TZ_SESSION_KEY] = timezone_name

        default_tz_name = get_current_timezone_name()
        # Simulate a timezone left active by a previous request on this thread.
        activate(pytz.timezone("Asia/Tokyo"))

        get_response = lambda x: HttpResponse("")
        TimezoneMiddleware(get_response).process_request(request)

        self.assertEqual(get_current_timezone_name(), default_tz_name)
        self.assertFalse(getattr(request, "timezone_active", False))
        self.assertNotIn(TZ_SESSION_KEY, request.session)
