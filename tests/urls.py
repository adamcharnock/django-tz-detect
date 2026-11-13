from django.urls import include
from django.urls import path

urlpatterns = [
    path("tz_detect/", include("tz_detect.urls")),
]
