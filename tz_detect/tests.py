from datetime import datetime

from pytz.tzinfo import BaseTzInfo

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware


class ViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def add_session(self, request):
        SessionMiddleware().process_request(request)

    def test_xhr_valid(self):
        from .views import SetOffsetView
        request = self.factory.post('/abc', {'offset': '-60'})
        self.add_session(request)
        
        response = SetOffsetView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('detected_tz', request.session)
        self.assertIsInstance(request.session['detected_tz'], BaseTzInfo)

    def test_xhr_bad_method(self):
        from .views import SetOffsetView
        request = self.factory.get('/abc')
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        self.assertEqual(response.status_code, 405)

    def test_xhr_no_offset(self):
        from .views import SetOffsetView
        request = self.factory.post('/abc')
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_xhr_bad_offset(self):
        from .views import SetOffsetView
        request = self.factory.post('/abc', {'offset': '12foo34'})
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        self.assertEqual(response.status_code, 400)


class OffsetToTimezoneTestCase(TestCase):

    def setUp(self):
        self.summer = datetime(2013, 06, 15, 12, 0, 0)
        self.winter = datetime(2013, 12, 15, 12, 0, 0)

    # Tests for various cities for both regular and daylight saving time
    def test_london_winter(self):
        from .utilities import offset_to_timezone
        tz = offset_to_timezone(0, now=self.winter)
        self.assertEqual(str(tz), 'Europe/London')

    def test_london_summer(self):
        from .utilities import offset_to_timezone
        tz = offset_to_timezone(-60, now=self.summer)
        self.assertEqual(str(tz), 'Europe/London')

    def test_new_york_winter(self):
        from .utilities import offset_to_timezone
        tz = offset_to_timezone(5*60, now=self.winter)
        self.assertEqual(str(tz), 'America/New_York')

    def test_new_york_summer(self):
        from .utilities import offset_to_timezone
        tz = offset_to_timezone(4*60, now=self.summer)
        self.assertEqual(str(tz), 'America/New_York')

    def test_tokyo(self):
        from .utilities import offset_to_timezone
        tz = offset_to_timezone(-9*60, now=self.summer)
        self.assertEqual(str(tz), 'Asia/Tokyo')

    def test_fuzzy(self):
        """Test the fuzzy matching of timezones"""
        from .utilities import offset_to_timezone
        tz = offset_to_timezone(-10, now=self.winter)
        self.assertEqual(str(tz), 'Europe/London')




