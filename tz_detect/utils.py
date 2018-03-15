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
    closest_tz = None
    closest_delta = 48 * 60  # Bigger than any possible timezone difference
    now = now or datetime.now()

    # JS offsets are flipped, so unflip.
    user_offset = -offset

    for tz_name in get_prioritized_timezones():
        tz = pytz.timezone(tz_name)
        try:
            tz_offset = tz.utcoffset(now).total_seconds() / 60
        except (pytz.NonExistentTimeError, pytz.AmbiguousTimeError):
            tz_offset = tz.localize(now, is_dst=False).utcoffset().total_seconds() / 60
        delta = abs(tz_offset - user_offset)
        if delta < closest_delta:
            closest_tz = tz
            closest_delta = delta
            if delta == 0:
                break

    return closest_tz


def convert_header_name(django_header):
    """Converts header name from django settings to real header name.

    For example:
    'HTTP_CUSTOM_CSRF' -> 'custom-csrf'
    """
    return django_header.lower().replace('_', '-').split('http-')[-1]
