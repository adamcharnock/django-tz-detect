from typing import Any

from django.contrib.auth.decorators import login_not_required
from django.http import HttpRequest
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View

from .defaults import TZ_SESSION_KEY
from .utils import is_valid_timezone


# The detection script runs for every visitor, including on the login page,
# so the endpoint must stay public under LoginRequiredMiddleware (#79).
@method_decorator(login_not_required, name="dispatch")
class SetOffsetView(View):
    http_method_names = ["post"]

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        timezone = request.POST.get("timezone", None)
        if is_valid_timezone(timezone):
            request.session[TZ_SESSION_KEY] = timezone
        else:
            if not request.POST.get("offset", None):
                return HttpResponse("No 'offset' parameter provided", status=400)

            try:
                offset = int(request.POST["offset"])
            except ValueError:
                return HttpResponse("Invalid 'offset' value provided", status=400)

            request.session[TZ_SESSION_KEY] = int(offset)

        return HttpResponse("OK")
