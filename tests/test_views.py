from datetime import timedelta
from http import HTTPStatus
from types import SimpleNamespace
from zoneinfo import ZoneInfo

from django import forms
from django.contrib.auth.middleware import LoginRequiredMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponse
from django.urls import reverse
from django.utils.timezone import activate
from django.utils.timezone import deactivate
from django.utils.timezone import get_current_timezone_name

import pytest

from tz_detect.defaults import TZ_SESSION_KEY
from tz_detect.middleware import TimezoneMiddleware
from tz_detect.views import SetOffsetView


def get_response(request):
    return HttpResponse("")


@pytest.fixture(autouse=True)
def deactivate_timezone():
    # The active timezone is thread-local; don't leak it into other tests.
    yield
    deactivate()


@pytest.fixture
def url_set():
    return reverse("tz_detect__set")


@pytest.fixture
def make_request(rf, url_set):
    def make_request(method="post", data=None):
        request = getattr(rf, method)(url_set, data or {})
        SessionMiddleware(get_response).process_request(request)
        return request

    return make_request


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        pytest.param({"offset": "-60"}, -60, id="offset"),
        pytest.param(
            {"timezone": "Europe/Amsterdam"},
            "Europe/Amsterdam",
            id="timezone",
        ),
        pytest.param(
            {"timezone": "Etc/GMT 3", "offset": "-180"},
            -180,
            id="invalid-timezone-fallback",
        ),
    ],
)
def test_view_stores_timezone(make_request, data, expected):
    request = make_request(data=data)

    response = SetOffsetView.as_view()(request)

    assert response.status_code == HTTPStatus.OK
    assert request.session[TZ_SESSION_KEY] == expected


@pytest.mark.parametrize(
    "data",
    [
        pytest.param({}, id="no-offset"),
        pytest.param({"offset": "12foo34"}, id="bad-offset"),
    ],
)
def test_view_bad_request(make_request, data):
    request = make_request(data=data)

    response = SetOffsetView.as_view()(request)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert TZ_SESSION_KEY not in request.session


def test_view_bad_method(make_request):
    request = make_request(method="get")

    response = SetOffsetView.as_view()(request)

    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_view_login_not_required(rf, url_set):
    # https://github.com/bashu/django-tz-detect/issues/79
    # LoginRequiredMiddleware (Django 5.1+) redirected anonymous visitors'
    # POSTs to the login page, so their timezone was never stored.
    request = rf.post(url_set, {"timezone": "Europe/Amsterdam"})
    request.user = SimpleNamespace(is_authenticated=False)

    middleware = LoginRequiredMiddleware(get_response)

    # None means the middleware lets the request through to the view.
    assert middleware.process_view(request, SetOffsetView.as_view(), (), {}) is None


def test_middleware_timezone_string(make_request):
    request = make_request(method="get")
    request.session[TZ_SESSION_KEY] = "Europe/Amsterdam"

    TimezoneMiddleware(get_response).process_request(request)

    assert get_current_timezone_name() == "Europe/Amsterdam"
    assert request.timezone_active is True


def test_middleware_invalid_timezone_string(make_request):
    request = make_request(method="get")
    request.session[TZ_SESSION_KEY] = "Etc/GMT 3"
    default_tz_name = get_current_timezone_name()
    # Simulate a timezone left active by a previous request on this thread.
    activate(ZoneInfo("Asia/Tokyo"))

    TimezoneMiddleware(get_response).process_request(request)

    assert get_current_timezone_name() == default_tz_name
    assert not hasattr(request, "timezone_active")
    assert TZ_SESSION_KEY not in request.session


def test_middleware_form_datetime_offset(make_request):
    # https://github.com/bashu/django-tz-detect/issues/80
    # With pytz zones, Django 5+ attached the zone's LMT offset (-07:53
    # for America/Los_Angeles) to datetimes submitted through forms.
    request = make_request(method="get")
    request.session[TZ_SESSION_KEY] = "America/Los_Angeles"

    TimezoneMiddleware(get_response).process_request(request)

    assert forms.DateTimeField().clean("2025-01-15 15:27").utcoffset() == timedelta(
        hours=-8,
    )
