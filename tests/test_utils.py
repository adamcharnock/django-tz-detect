from datetime import UTC
from datetime import datetime

import pytest

from tz_detect.utils import convert_header_name
from tz_detect.utils import offset_to_timezone

SUMMER = datetime(2013, 6, 15, 12, 0, 0, tzinfo=UTC)
WINTER = datetime(2013, 12, 15, 12, 0, 0, tzinfo=UTC)


# Note: These hours are in JavaScript's Date.getTimezoneOffset() convention,
# so the sign is reversed compared to conventional UTC offset notation.
@pytest.mark.parametrize(
    ("js_offset_hours", "expected_tzs"),
    [
        (12, ("Pacific/Midway", "Pacific/Midway")),
        (11, ("Pacific/Midway", "Pacific/Midway")),
        # USA:
        (10, ("America/Adak", "Pacific/Honolulu")),  # HST, HST
        (9, ("America/Anchorage", "America/Adak")),  # AKST, HDT
        (8, ("America/Los_Angeles", "America/Anchorage")),  # PST, AKDT
        (7, ("America/Denver", "America/Phoenix")),  # MST, PDT
        (6, ("America/Chicago", "America/Denver")),  # CST, MDT
        (5, ("America/New_York", "America/Chicago")),  # EST, CDT
        (4, ("America/Porto_Velho", "America/New_York")),  # AMT, EDT
        (3, ("America/Belem", "America/Belem")),
        (2, ("America/Noronha", "America/Noronha")),
        (1, ("America/Scoresbysund", "Atlantic/Cape_Verde")),
        # Central Europe:
        (0, ("Europe/London", "Africa/Abidjan")),  # GMT, GMT
        (-1, ("Europe/Berlin", "Europe/London")),  # CET, BST
        (-2, ("Europe/Kaliningrad", "Europe/Kaliningrad")),
        (-3, ("Europe/Moscow", "Europe/Moscow")),
        (-4, ("Europe/Astrakhan", "Europe/Astrakhan")),
        (-5, ("Asia/Yekaterinburg", "Asia/Yekaterinburg")),
        (-6, ("Asia/Urumqi", "Asia/Urumqi")),
        (-7, ("Asia/Novosibirsk", "Asia/Novosibirsk")),
        (-8, ("Asia/Shanghai", "Asia/Shanghai")),
        (-9, ("Asia/Tokyo", "Asia/Tokyo")),
        (-10, ("Asia/Vladivostok", "Asia/Vladivostok")),
        (-11, ("Asia/Magadan", "Asia/Magadan")),
        (-12, ("Asia/Kamchatka", "Asia/Kamchatka")),
        (-13, ("Antarctica/McMurdo", "Pacific/Apia")),
        (-14, ("Pacific/Apia", "Pacific/Kiritimati")),
    ],
)
def test_offset_to_timezone_hourly(js_offset_hours, expected_tzs):
    js_offset_minutes = js_offset_hours * 60

    actual_tzs = (
        str(
            offset_to_timezone(js_offset_minutes, datetime(2018, 1, 1, tzinfo=UTC)),
        ),  # Start/end of year
        str(
            offset_to_timezone(js_offset_minutes, datetime(2018, 7, 1, tzinfo=UTC)),
        ),  # Mid-year
    )

    assert actual_tzs == expected_tzs


@pytest.mark.parametrize(
    ("js_offset_minutes", "now", "expected"),
    [
        pytest.param(0, WINTER, "Europe/London", id="london-winter"),
        pytest.param(-60, SUMMER, "Europe/London", id="london-summer"),
        pytest.param(5 * 60, WINTER, "America/New_York", id="new-york-winter"),
        pytest.param(4 * 60, SUMMER, "America/New_York", id="new-york-summer"),
        pytest.param(-9 * 60, SUMMER, "Asia/Tokyo", id="tokyo"),
        pytest.param(-10, WINTER, "Europe/London", id="fuzzy"),
    ],
)
def test_offset_to_timezone(js_offset_minutes, now, expected):
    assert str(offset_to_timezone(js_offset_minutes, now=now)) == expected


@pytest.mark.parametrize(
    ("django_header", "expected"),
    [
        pytest.param("HTTP_X_CSRFTOKEN", "x-csrftoken", id="default"),
        pytest.param("HTTP_X_XSRF_TOKEN", "x-xsrf-token", id="custom"),
        pytest.param("X_XSRF_TOKEN", "x-xsrf-token", id="no-http-prefix"),
    ],
)
def test_convert_header_name(django_header, expected):
    assert convert_header_name(django_header) == expected
