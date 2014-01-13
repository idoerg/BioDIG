from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('', 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'web.public.views.applications.Media.Application.renderAction', {'document_root': settings.MEDIA_ROOT}),
)

urlpatterns += patterns('',
    url(r'^api/', include('rest.v1.urls')),
    url(r'^rest/', include('rest.urls')),
    url(r'', include('web.urls'))
)
