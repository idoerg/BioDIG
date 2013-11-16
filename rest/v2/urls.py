from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('rest.v2.views',
    url(r'^tagGroups$', 'TagGroups.multiple.Application.renderAction'),
    url(r'^tagGroups/(\d+)$', 'TagGroups.single.Application.renderAction'),
    url(r'^tags$', 'Tags.multiple.Application.renderAction'),
    url(r'^tags/(\d+)$', 'Tags.single.Application.renderAction'),
    url(r'^organism$', 'Organism.multiple.Application.renderAction'),
    url(r'^organism/(\d+)$', 'Organism.single.Application.renderAction'),
    url(r'^geneLinks$', 'GeneLinks.multiple.Application.renderAction'),
    url(r'^geneLinks/(\d+)$', 'GeneLinks.single.Application.renderAction')
)

urlpatterns += patterns('',
    url(r'^users/token$', 'rest_framework.authtoken.views.obtain_auth_token')
)
