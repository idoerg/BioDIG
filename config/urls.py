from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('', 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'biodig.web.public.views.applications.Media.Application.renderAction', {'document_root': settings.MEDIA_ROOT}),
)

urlpatterns += patterns('',
    url(r'^rest/', include('biodig.rest.urls')),
    url(r'', include('biodig.web.urls'))
)
