from django.conf.urls import patterns, url

from biodig.rest.v2.Images.views import ImageList, ImageSingle
from biodig.rest.v2.ImageOrganisms.views import ImageOrganismList, ImageOrganismSingle
from biodig.rest.v2.TagGroups.views import TagGroupList, TagGroupSingle
from biodig.rest.v2.Tags.views import TagList, TagSingle
from biodig.rest.v2.GeneLinks.views import GeneLinkList, GeneLinkSingle

urlpatterns = patterns('',
    url(r'^images/(\d+)/tagGroups/(\d+)/tags/(\d+)/geneLinks/(\d+)/?$', GeneLinkSingle.as_view(), name="Gene Links Single View"),
    url(r'^images/(\d+)/tagGroups/(\d+)/tags/(\d+)/geneLinks/?$', GeneLinkList.as_view(), name="Gene Links Multiple View"),
    url(r'^images/(\d+)/tagGroups/(\d+)/tags/(\d+)/?$', TagSingle.as_view(), name="Tag Single View"),
    url(r'^images/(\d+)/tagGroups/(\d+)/tags/?$', TagList.as_view(), name="Tag Multiple View"),
    url(r'^images/(\d+)/tagGroups/(\d+)/?$', TagGroupSingle.as_view(), name="Tag Group Single View"),
    url(r'^images/(\d+)/tagGroups/?$', TagGroupList.as_view(), name="Tag Group Multiple View"),
    url(r'^images/(\d+)/organisms/(\d+)/?$', ImageOrganismSingle.as_view(), name="Image Organism Single View"),
    url(r'^images/(\d+)/organisms/?$', ImageOrganismList.as_view(), name="Image Organism Multiple View"),
    url(r'^images/(\d+)/?$', ImageSingle.as_view(), name="Image Single View"),
    url(r'^images/?$', ImageList.as_view(), name="Image Multiple View")
    #url(r'^organism$', 'Organism.multiple.Application.renderAction'),
    #url(r'^organism/(\d+)$', 'Organism.single.Application.renderAction'),
    #url(r'^geneLinks$', 'GeneLinks.multiple.Application.renderAction'),
    #url(r'^geneLinks/(\d+)$', 'GeneLinks.single.Application.renderAction')
)

urlpatterns += patterns('',
    url(r'^users/token/?$', 'rest_framework.authtoken.views.obtain_auth_token')
)
