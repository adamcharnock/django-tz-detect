from django.conf.urls import patterns, include, url

from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^tz_detect/', include('tz_detect.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
)
