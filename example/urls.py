from django.conf.urls import include, path

from django.views.generic import TemplateView

urlpatterns = [
    path('tz_detect/', include('tz_detect.urls')),
    path('', TemplateView.as_view(template_name='index.html')),
]
