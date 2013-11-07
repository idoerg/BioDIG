from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'', include('web.public.urls')),
    url(r'^administration/', include('web.registered.urls'))
)
