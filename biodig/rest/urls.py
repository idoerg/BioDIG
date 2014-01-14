from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^v1/', include('biodig.rest.v1.urls')),
    url(r'^v2/', include('biodig.rest.v2.urls'))
)
