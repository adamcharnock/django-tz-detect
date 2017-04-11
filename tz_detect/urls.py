# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .views import SetOffsetView

urlpatterns = [
    url(r'^set/$', csrf_exempt(SetOffsetView.as_view()), name="tz_detect__set"),
]
