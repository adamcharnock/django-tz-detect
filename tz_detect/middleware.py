from django.utils import timezone


class TimezoneMiddleware(object):
    def process_request(self, request):
        # import pdb; pdb.set_trace();
        tz = request.session.get('detected_tz')
        if tz:
            request.timezone_active = True
            timezone.activate(tz)
        else:
            timezone.deactivate()
