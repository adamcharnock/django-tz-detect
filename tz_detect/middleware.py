from zoneinfo import ZoneInfo

from django.utils import timezone

from .defaults import TZ_SESSION_KEY

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:  # Django < 1.10
    MiddlewareMixin = object

from .utils import is_valid_timezone
from .utils import offset_to_timezone


class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        tz = request.session.get(TZ_SESSION_KEY)
        if tz:
            if self._try_to_set_timezone(tz):
                # ``request.timezone_active`` is used in the template tag
                # to detect if the timezone has been activated
                request.timezone_active = True
            else:
                # The stored value is unusable: reset the thread-local
                # timezone so it doesn't leak from a previous request, and
                # drop the value so the browser re-detects it.
                timezone.deactivate()
                request.session.pop(TZ_SESSION_KEY, None)
        else:
            timezone.deactivate()

    def _try_to_set_timezone(self, tz):
        if isinstance(tz, str):
            if not is_valid_timezone(tz):
                return False
            timezone.activate(ZoneInfo(tz))
        else:
            timezone.activate(offset_to_timezone(tz))

        return True
