from django.conf.urls import patterns, url

from biodig.rest.v2.Users.views import UserList, UserSingle, UserActivation
from biodig.rest.v2.Organisms.views import OrganismList, OrganismSingle
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
    url(r'^images/?$', ImageList.as_view(), name="Image Multiple View"),
    url(r'^organisms/(\d+)/?$', OrganismSingle.as_view(), name="Organism Single View"),
    url(r'^organisms/?$', OrganismList.as_view(), name="Organism List View")
)

urlpatterns += patterns('',
    url(r'^users/token/?$', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^users/(\d+)/activate/([-\w]+)/?$', UserActivation.as_view(), name="User Activation View"),
    url(r'^users/(\d+)/?$', UserSingle.as_view(), name="User Single View"),
    url(r'^users/?$', UserList.as_view(), name="User List View")
)
