from django.conf.urls import patterns, url

from biodig.rest.beetles.Orthologs.views import OrthologList, OrthologSingle

urlpatterns = patterns('',
    url(r'^orthologs/?$', OrthologList.as_view(), name="OrthologListView"),
    url(r'^orthologs/(\w\w[\w]+)/?$', OrthologSingle.as_view(), name="Ortholog Single View")
)

