from django.utils import timezone


class TimezoneMiddleware(object):
    def process_request(self, request):
        tz = request.session.get('detected_tz')
        if tz:
            # `request.timezone_active` is used in the template
            # tag to detect if the timezone has been activated
            request.timezone_active = True
            timezone.activate(tz)
        else:
            timezone.deactivate()
