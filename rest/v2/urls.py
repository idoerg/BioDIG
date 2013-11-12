from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('rest.v2.views',
    url(r'^tagGroups$', 'TagGroups.multiple.Application.renderAction'),
    url(r'^tagGroups/(\d+)$', 'TagGroups.single.Application.renderAction')
)

urlpatterns += patterns('',
    url(r'^users/token$', 'rest_framework.authtoken.views.obtain_auth_token')
)
