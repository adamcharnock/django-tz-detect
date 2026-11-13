from tz_detect.templatetags.tz_detect import tz_detect


def test_no_request_in_context():
    result = tz_detect({})

    assert result["show"] is True
