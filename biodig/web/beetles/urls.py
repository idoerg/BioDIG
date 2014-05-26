from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('biodig.web.beetles.views.applications',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^orthologs/(\w\w_[\w]+)/?$', 'OrthologViewer.Application.renderAction'),
)
