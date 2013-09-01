import logging

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.utils.http import is_safe_url

from tz_detect.utilities import offset_to_timezone
from tz_detect.defaults import TZ_DEFAULT_RELOAD_URL, TZ_RELOAD

logger = logging.getLogger('tz_detect')


class SetOffsetView(View):
    """ Handle the setting of the user's timezone offset in their session

    This view handles two cases:

        1) Request via Ajax
        2) Browser accessing the endpoint directly
    
    In the case of the former, we return errors as appropriate. For the 
    latter, we always make sure we redirect the user onwards in a 
    pleasent way (as we don't want to break the entire site due to a 
    timezone error).

    """
    http_method_names = ['post', 'get']

    def get_offset(self, request):
        """Get the offset from the request"""
        offset = request.REQUEST.get('offset', None)
        if not offset:
            raise ValueError("No 'offset' parameter provided")

        try:
            offset = int(offset)
        except ValueError:
            raise ValueError("Invalid 'offset' value provided")

        return offset

    def get_redirect(self, request):
        """Get a HttpResponseRedirect to use when TZ_RELOAD=True"""
        next = request.REQUEST.get('next', None)
        if next and not is_safe_url(next):
            next = None

        next = next or TZ_DEFAULT_RELOAD_URL
        return HttpResponseRedirect(next)

    def set_timezone(self, request):
        """Get the offset for the given request
        and set the timezone on the request's session"""
        try:
            offset = self.get_offset(request)
        except ValueError, e:
            logger.exception(e)
            if request.is_ajax():
                return HttpResponse(str(e), status=400)
            else:
                return self.get_redirect(request)

        tz = offset_to_timezone(int(offset))
        request.session['detected_tz'] = tz

        if request.is_ajax():
            return HttpResponse("OK")
        else:
            return self.get_redirect(request)

    def post(self, request, *args, **kwargs):
        return self.set_timezone(request)

    def get(self, request, *args, **kwargs):
        # Get requests not allowed for ajax requests or if TZ_RELOAD is disabled
        if request.is_ajax() or not TZ_RELOAD:
            return self.http_method_not_allowed(request, *args, **kwargs)

        return self.set_timezone(request)

    def http_method_not_allowed(self, request, *args, **kwargs):
        # Just add a little logging here
        logger.error('Invalid HTTP method when setting timezone.')
        return super(SetOffsetView, self).http_method_not_allowed(request, *args, **kwargs)
