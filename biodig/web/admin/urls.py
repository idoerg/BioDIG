from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('biodig.web.admin.views.applications',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^dashboard/?$', 'Dashboard.Application.renderAction'),
)
