from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('biodig.web.public.views.applications',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', 'Home.Application.renderAction'),
    url(r'^index.html$', 'Home.Application.renderAction'),
    url(r'^images/viewer/(\d+)/?$','ViewImage.Application.renderAction'),
    url(r'^images/?$', 'Images.Application.renderAction'),
    url(r'^genome_browser/?$', 'GBrowse.Application.renderAction'),
    url(r'^login/?$', 'Login.Application.renderAction'),
    url(r'^logout/?$', 'Logout.Application.renderAction'),
    url(r'^search/?$', 'Search.Application.renderAction'),
    url(r'^advancedSearch/?$', 'AdvancedSearch.Application.renderAction'),
    url(r'^activate/(\d+)/([-\w]+)/?$', 'Activate.Application.renderAction')
)
