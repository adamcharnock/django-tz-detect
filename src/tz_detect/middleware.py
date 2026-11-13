from zoneinfo import ZoneInfo

from django.http import HttpRequest
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from .defaults import TZ_SESSION_KEY
from .utils import is_valid_timezone
from .utils import offset_to_timezone


class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest) -> None:
        tz = request.session.get(TZ_SESSION_KEY)
        if tz:
            if self._try_to_set_timezone(tz):
                # ``request.timezone_active`` is used in the template tag
                # to detect if the timezone has been activated
                request.timezone_active = True  # type: ignore[attr-defined]
            else:
                # The stored value is unusable: reset the thread-local
                # timezone so it doesn't leak from a previous request, and
                # drop the value so the browser re-detects it.
                timezone.deactivate()
                request.session.pop(TZ_SESSION_KEY, None)
        else:
            timezone.deactivate()

    def _try_to_set_timezone(self, tz: str | int) -> bool:
        if isinstance(tz, str):
            if not is_valid_timezone(tz):
                return False
            timezone.activate(ZoneInfo(tz))
        else:
            timezone.activate(offset_to_timezone(tz))

        return True
