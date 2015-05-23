# -*- coding: utf-8 -*-

import pytz
from itertools import chain
from datetime import datetime

from django.utils import timezone

from .defaults import TZ_DETECT_COUNTRIES


def get_prioritized_timezones():
    def tz_gen():
        for c in TZ_DETECT_COUNTRIES:
            yield pytz.country_timezones(c)
        yield pytz.common_timezones

    return chain.from_iterable(tz_gen())


def offset_to_timezone(offset, now=None):
    """Convert a minutes offset (JavaScript-style) into a pytz timezone

    The ``now`` parameter is generally used for testing only
    """
    clostest_tz = None
    clostest_delta = 1440
    now = now or datetime.now()

    # JS offsets are flipped and can be negative, so
    # unflip and put into range 0 - 1440
    user_offset = (offset * -1)
    user_offset = (user_offset + 1440) % 1440

    for tz_name in get_prioritized_timezones():
        tz = pytz.timezone(tz_name)
        try:
            tz_offset = tz.utcoffset(now).seconds / 60
        except (pytz.NonExistentTimeError, pytz.AmbiguousTimeError):
            tz_offset = tz.localize(now, is_dst=False).utcoffset().seconds / 60
        delta = tz_offset - user_offset
        if abs(delta) < abs(clostest_delta):
            clostest_tz = tz
            clostest_delta = delta
            if delta == 0:
                break

    return clostest_tz
