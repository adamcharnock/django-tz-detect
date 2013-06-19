from django.conf.urls import patterns, url

from tz_detect.views import SetOffsetView

urlpatterns = patterns('',
    url(r'^set/$', SetOffsetView.as_view(), name="tz_detect__set"),
)
