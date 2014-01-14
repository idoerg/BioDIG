from django.conf.urls import patterns, include, url
from django.conf import settings

from biodig.rest.v2.TagGroups.views import TagGroupList, TagGroupSingle

urlpatterns = patterns('',
    url(r'^tagGroups$', TagGroupList.as_view(), name="Tag Group Multiple View"),
    url(r'^tagGroups/(\d+)$', TagGroupSingle.as_view(), name="Tag Group Single View"),
    #url(r'^tags$', 'Tags.multiple.Application.renderAction'),
    #url(r'^tags/(\d+)$', 'Tags.single.Application.renderAction'),
    #url(r'^organism$', 'Organism.multiple.Application.renderAction'),
    #url(r'^organism/(\d+)$', 'Organism.single.Application.renderAction'),
    #url(r'^geneLinks$', 'GeneLinks.multiple.Application.renderAction'),
    #url(r'^geneLinks/(\d+)$', 'GeneLinks.single.Application.renderAction')
)

urlpatterns += patterns('',
    url(r'^users/token$', 'rest_framework.authtoken.views.obtain_auth_token')
)
