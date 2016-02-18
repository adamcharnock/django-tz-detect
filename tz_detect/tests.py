# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase
from django.test.client import RequestFactory
from pytz.tzinfo import BaseTzInfo

from tz_detect.templatetags.tz_detect import tz_detect
from tz_detect.utils import offset_to_timezone
from tz_detect.views import SetOffsetView


class ViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def add_session(self, request):
        SessionMiddleware().process_request(request)

    def test_xhr_valid(self):
        request = self.factory.post('/abc', {'offset': '-60'})
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('detected_tz', request.session)
        self.assertIsInstance(request.session['detected_tz'], int)

    def test_xhr_bad_method(self):
        request = self.factory.get('/abc')
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        self.assertEqual(response.status_code, 405)

    def test_xhr_no_offset(self):
        request = self.factory.post('/abc')
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_xhr_bad_offset(self):
        request = self.factory.post('/abc', {'offset': '12foo34'})
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        self.assertEqual(response.status_code, 400)


class OffsetToTimezoneTestCase(TestCase):

    def setUp(self):
        self.summer = datetime(2013, 6, 15, 12, 0, 0)
        self.winter = datetime(2013, 12, 15, 12, 0, 0)

    # Tests for various cities for both regular and daylight saving time
    def test_london_winter(self):
        tz = offset_to_timezone(0, now=self.winter)
        self.assertEqual(str(tz), 'Europe/London')

    def test_london_summer(self):
        tz = offset_to_timezone(-60, now=self.summer)
        self.assertEqual(str(tz), 'Europe/London')

    def test_new_york_winter(self):
        tz = offset_to_timezone(5*60, now=self.winter)
        self.assertEqual(str(tz), 'America/New_York')

    def test_new_york_summer(self):
        tz = offset_to_timezone(4*60, now=self.summer)
        self.assertEqual(str(tz), 'America/New_York')

    def test_tokyo(self):
        tz = offset_to_timezone(-9*60, now=self.summer)
        self.assertEqual(str(tz), 'Asia/Tokyo')

    def test_fuzzy(self):
        """Test the fuzzy matching of timezones"""
        tz = offset_to_timezone(-10, now=self.winter)
        self.assertEqual(str(tz), 'Europe/London')


class TemplatetagTestCase(TestCase):

    def test_no_request_context(self):
        try:
            tz_detect({})
        except KeyError as e:
            if e.message == 'request':
                self.fail("Templatetag shouldn't expect request in context.")
            else:
                raise
