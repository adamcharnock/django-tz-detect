# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import SetOffsetView

urlpatterns = patterns('',
    url(r'^set/$', SetOffsetView.as_view(), name="tz_detect__set"),
)
