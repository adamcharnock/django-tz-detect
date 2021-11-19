from django.conf.urls import path
from django.urls import include
from django.views.generic import TemplateView

urlpatterns = [
    path("tz_detect/", include("tz_detect.urls")),
    path("", TemplateView.as_view(template_name="index.html")),
]
