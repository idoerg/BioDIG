from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'', include('biodig.web.public.urls')),
    url(r'^administration/', include('biodig.web.registered.urls'))
)
