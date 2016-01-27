from django.conf.urls import include, url

from django.views.generic import TemplateView

urlpatterns = [
    url(r'^tz_detect/', include('tz_detect.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
]
