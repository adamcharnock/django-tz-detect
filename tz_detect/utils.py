import contextlib
import pathlib
from datetime import datetime
from functools import lru_cache
from importlib import resources
from itertools import chain
from zoneinfo import TZPATH, ZoneInfo, ZoneInfoNotFoundError, available_timezones

from .defaults import TZ_DETECT_COUNTRIES


@lru_cache(maxsize=1)
def country_timezones():
    """Map ISO 3166 country codes to the timezone names used in that country,
    in place of ``pytz.country_timezones``.

    Ported from pytz (MIT licence): parses the IANA ``zone.tab`` file the
    same way. Looks in the same places, in the same order, as ``ZoneInfo``:
    the system timezone database (``zoneinfo.TZPATH``) first, then the
    ``tzdata`` package if it happens to be installed.

    Cached (per-process) since it reads ``zone.tab`` from disk.
    """
    tzpath = [pathlib.Path(p) for p in TZPATH]
    with contextlib.suppress(ModuleNotFoundError):
        tzpath.append(resources.files("tzdata").joinpath("zoneinfo"))

    zones = {}
    for path in tzpath:
        try:
            zone_file = path.joinpath("zone.tab").open("r", encoding="utf-8")
        except FileNotFoundError:
            continue

        with zone_file:
            for line in zone_file:
                if line.startswith("#"):
                    continue
                code, _coordinates, zone = line.split(None, 4)[:3]
                zones.setdefault(code, []).append(zone)
        break

    return zones


@lru_cache(maxsize=1)
def common_timezones():
    """A subset of ``zoneinfo.available_timezones()``, used in place of
    ``pytz.common_timezones``.

    Drops non-geographic zones (``Etc/GMT+5``), the ``posix/``, ``right/``
    and ``SystemV/`` copies of the database, and bare abbreviations with no
    ``/`` (``EST``), so that offset_to_timezone() picks real places, as it
    did with pytz. Unlike pytz's list, deprecated aliases with a ``/``
    (``America/Buenos_Aires``) are kept.

    Sorted, so that ties in offset_to_timezone() resolve the same way every
    time. Cached (per-process) since ``available_timezones()`` scans the
    whole timezone database on every call.
    """
    names = {
        name
        for name in available_timezones()
        if "/" in name and not name.startswith(("Etc/", "posix/", "right/", "SystemV/"))
    }
    names.update(("UTC", "GMT"))
    return sorted(names)


def get_prioritized_timezones():
    def tz_gen():
        for c in TZ_DETECT_COUNTRIES:
            # pytz accepted lowercase codes too, e.g. "ch".
            yield country_timezones()[c.upper()]
        yield common_timezones()

    return chain.from_iterable(tz_gen())


def offset_to_timezone(offset, now=None):
    """Convert a minutes offset (JavaScript-style) into a ``ZoneInfo`` timezone

    The ``now`` parameter is generally used for testing only
    """
    now = now or datetime.now()

    # JS offsets are flipped, so unflip.
    user_offset = -offset

    # Helper: timezone offset in minutes
    def get_tz_offset(tz):
        return tz.utcoffset(now).total_seconds() / 60

    def get_zones():
        for tz_name in get_prioritized_timezones():
            # Skip any name the timezone database can't load.
            try:
                yield ZoneInfo(tz_name)
            except ZoneInfoNotFoundError:
                continue

    # Return the timezone with the minimum difference to the user's offset.
    return min(
        get_zones(),
        key=lambda tz: abs(get_tz_offset(tz) - user_offset),
    )


def convert_header_name(django_header):
    """Converts header name from django settings to real header name.

    For example:
    'HTTP_CUSTOM_CSRF' -> 'custom-csrf'
    """
    return django_header.lower().replace("_", "-").split("http-")[-1]


def is_valid_timezone(timezone):
    """Check if a given string can be used as a timezone."""
    if not timezone:
        return False

    try:
        ZoneInfo(timezone)
        return True
    except (ZoneInfoNotFoundError, ValueError):
        # ValueError: malformed keys, such as "../etc/passwd".
        return False
