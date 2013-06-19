from django.http import HttpResponse
from django.views.generic import View

from tz_detect.utilities import offset_to_timezone


class SetOffsetView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        offset = request.POST.get('offset', None)
        if not offset:
            return HttpResponse("No 'offset' parameter provided", status_code=400)

        try:
            offset = int(offset)
        except ValueError:
            return HttpResponse("Invalid 'offset' value provided", status_code=400)

        tz = offset_to_timezone(int(offset))
        request.session['detected_tz'] = tz

        return HttpResponse("OK")
