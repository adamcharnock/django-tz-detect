from collections.abc import Sequence

from django.conf import settings

# These countries will be prioritised in the search
# for a matching timezone. Consider putting your
# app's most popular countries first.
# Defaults to top Internet using countries.

TZ_DETECT_COUNTRIES: Sequence[str] = getattr(
    settings,
    "TZ_DETECT_COUNTRIES",
    ("CN", "US", "IN", "JP", "BR", "RU", "DE", "FR", "GB"),
)


# Session key to use to store the detected timezone
TZ_SESSION_KEY: str = getattr(settings, "TZ_SESSION_KEY", "detected_tz")


# Reload the page once the detected timezone is stored, so the first
# page view is shown in the visitor's timezone too.
TZ_DETECT_RELOAD: bool = getattr(settings, "TZ_DETECT_RELOAD", False)
