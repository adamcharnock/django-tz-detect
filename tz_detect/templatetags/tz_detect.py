from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('tz_detect/detector.html', takes_context=True)
def tz_detect(context):
    return {
        'show': not hasattr(context['request'], 'timezone_active'),
        'STATIC_URL': settings.STATIC_URL,
        'DEBUG': settings.DEBUG,
    }
