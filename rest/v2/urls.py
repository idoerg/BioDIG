from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('rest.v2.views',
    url(r'^tagGroups$', 'TagGroups.multiple.Application.renderAction'),
    url(r'^api/tagGroups/(\d+)$', 'TagGroups.single.Application.renderAction')
)
