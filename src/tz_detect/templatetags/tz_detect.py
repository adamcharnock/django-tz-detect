from typing import Any

from django import template
from django.conf import settings
from django.template import Context

from tz_detect import defaults
from tz_detect.utils import convert_header_name

register = template.Library()


@register.inclusion_tag("tz_detect/detector.html", takes_context=True)
def tz_detect(context: Context, **script_attrs: Any) -> dict[str, Any]:
    request = context.get("request")
    return {
        "show": not hasattr(request, "timezone_active"),
        # Reloading a page rendered for a POST would make the browser resubmit the form.
        "reload": defaults.TZ_DETECT_RELOAD
        and getattr(request, "method", None) == "GET",
        "debug": getattr(settings, "DEBUG", False),
        "csrf_header_name": convert_header_name(
            getattr(settings, "CSRF_HEADER_NAME", "HTTP_X_CSRFTOKEN"),
        ),
        "script_attrs": script_attrs,
    }
