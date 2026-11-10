from datetime import timedelta
from http import HTTPStatus
from types import SimpleNamespace
from zoneinfo import ZoneInfo

from django import forms
from django.contrib.auth.middleware import LoginRequiredMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.timezone import activate
from django.utils.timezone import deactivate
from django.utils.timezone import get_current_timezone_name

from tz_detect.defaults import TZ_SESSION_KEY
from tz_detect.middleware import TimezoneMiddleware
from tz_detect.views import SetOffsetView


def get_response(request):
    return HttpResponse("")


class ViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def add_session(self, request):
        SessionMiddleware(get_response).process_request(request)

    def test_xhr_valid_offset(self):
        request = self.factory.post("/abc", {"offset": "-60"})
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        assert response.status_code == HTTPStatus.OK
        assert TZ_SESSION_KEY in request.session
        assert isinstance(request.session[TZ_SESSION_KEY], int)

    def test_xhr_valid_timezone(self):
        timezone_name = "Europe/Amsterdam"
        request = self.factory.post("/abc", {"timezone": timezone_name})
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        assert response.status_code == HTTPStatus.OK
        assert TZ_SESSION_KEY in request.session
        assert request.session[TZ_SESSION_KEY] == timezone_name

    def test_xhr_invalid_timezone_fallback(self):
        timezone_name = "Etc/GMT 3"
        offset = -180
        request = self.factory.post(
            "/abc",
            {"timezone": timezone_name, "offset": str(offset)},
        )
        self.add_session(request)
        response = SetOffsetView.as_view()(request)

        assert response.status_code == HTTPStatus.OK
        assert TZ_SESSION_KEY in request.session
        assert request.session[TZ_SESSION_KEY] == offset

    def test_xhr_bad_method(self):
        request = self.factory.get("/abc")
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_xhr_no_offset(self):
        request = self.factory.post("/abc")
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_xhr_bad_offset(self):
        request = self.factory.post("/abc", {"offset": "12foo34"})
        self.add_session(request)

        response = SetOffsetView.as_view()(request)
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_middleware_timezone_string(self):
        timezone_name = "Europe/Amsterdam"
        request = self.factory.post("/abc", {"timezone": timezone_name})
        self.add_session(request)
        request.session[TZ_SESSION_KEY] = timezone_name

        TimezoneMiddleware(get_response).process_request(request)
        tz_name = get_current_timezone_name()
        assert tz_name == timezone_name

    def test_middleware_invalid_timezone_string(self):
        timezone_name = "Etc/GMT 3"
        request = self.factory.post("/abc", {"timezone": timezone_name})
        self.add_session(request)
        request.session[TZ_SESSION_KEY] = timezone_name

        default_tz_name = get_current_timezone_name()
        # Simulate a timezone left active by a previous request on this thread.
        activate(ZoneInfo("Asia/Tokyo"))

        TimezoneMiddleware(get_response).process_request(request)

        assert get_current_timezone_name() == default_tz_name
        assert not getattr(request, "timezone_active", False)
        assert TZ_SESSION_KEY not in request.session

    def test_middleware_form_datetime_offset(self):
        # https://github.com/adamcharnock/django-tz-detect/issues/80
        # With pytz zones, Django 5+ attached the zone's LMT offset (-07:53
        # for America/Los_Angeles) to datetimes submitted through forms.
        timezone_name = "America/Los_Angeles"
        request = self.factory.get("/abc")
        self.add_session(request)
        request.session[TZ_SESSION_KEY] = timezone_name

        TimezoneMiddleware(get_response).process_request(request)
        # The active timezone is thread-local; don't leak it into other tests.
        self.addCleanup(deactivate)

        assert forms.DateTimeField().clean("2025-01-15 15:27").utcoffset() == timedelta(
            hours=-8,
        )

    def test_view_login_not_required(self):
        # https://github.com/adamcharnock/django-tz-detect/issues/79
        # LoginRequiredMiddleware (Django 5.1+) redirected anonymous visitors'
        # POSTs to the login page, so their timezone was never stored.
        request = self.factory.post("/abc", {"timezone": "Europe/Amsterdam"})
        request.user = SimpleNamespace(is_authenticated=False)

        middleware = LoginRequiredMiddleware(get_response)
        # None means the middleware lets the request through to the view.
        assert middleware.process_view(request, SetOffsetView.as_view(), (), {}) is None
