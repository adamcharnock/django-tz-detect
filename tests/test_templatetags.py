from django.template import Context
from django.template import Template

import pytest

from tz_detect import defaults
from tz_detect.templatetags.tz_detect import tz_detect


def test_no_request_in_context():
    result = tz_detect({})

    assert result["show"] is True


@pytest.mark.parametrize(
    ("enabled", "method", "expected"),
    [
        pytest.param(True, "get", True, id="enabled"),
        pytest.param(True, "post", False, id="enabled-post"),
        pytest.param(False, "get", False, id="disabled"),
    ],
)
def test_reload(rf, monkeypatch, enabled, method, expected):
    monkeypatch.setattr(defaults, "TZ_DETECT_RELOAD", enabled)
    request = getattr(rf, method)("/")

    html = Template("{% load tz_detect %}{% tz_detect %}").render(
        Context({"request": request}),
    )

    assert ("data-reload" in html) is expected
