from django.http import HttpResponse
from django.views.generic import View

from .defaults import TZ_SESSION_KEY
from .utils import is_valid_timezone


class SetOffsetView(View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        timezone = request.POST.get("timezone", None)
        if is_valid_timezone(timezone):
            request.session[TZ_SESSION_KEY] = timezone
        else:
            offset = request.POST.get("offset", None)
            if not offset:
                return HttpResponse("No 'offset' parameter provided", status=400)

            try:
                offset = int(offset)
            except ValueError:
                return HttpResponse("Invalid 'offset' value provided", status=400)

            request.session[TZ_SESSION_KEY] = int(offset)

        return HttpResponse("OK")
