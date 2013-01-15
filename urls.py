from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('taxon_home.views.applications.public',
    # Examples:
    # url(r'^$', 'mycoplasma_site.views.home', name='home'),
    # url(r'^mycoplasma_site/', include('mycoplasma_site.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', 'Home.Application.renderAction'),
    url(r'^index.html$', 'Home.Application.renderAction'),
    url(r'^images/editor$','EditImage.Application.renderAction'),
    url(r'^images/$', 'Images.Application.renderAction'),
    url(r'^genome_browser/$', 'GBrowse.Application.renderAction'),
    url(r'^blast/$', 'Blast.Application.renderAction'),
    #url(r'^blast/submit/$', 'mycoplasma_home.views.submit_blast'),
    url(r'^login_handler/$', 'Login.Application.renderAction'),
    url(r'^logout_handler/$', 'Logout.Application.renderAction'),
    url(r'^search/$', 'Search.Application.renderAction')
)

urlpatterns += patterns('taxon_home.views.webServices',
    url(r'^api/tags$', 'Tags.Application.renderAction'),
    url(r'^api/tagGroups$', 'TagGroups.Application.renderAction'),
    url(r'^api/imageMetadata$', 'ImageMetadata.Application.renderAction'),
    url(r'^api/geneLinks/search$', 'SearchGeneLinks.Application.renderAction'),
    url(r'^api/tags/search$', 'SearchTags.Application.renderAction'),
    url(r'^api/tagGroups/search$', 'SearchTagGroups.Application.renderAction'),
    url(r'^api/imageMetadata/search$', 'SearchImageMetadata.Application.renderAction')
)

urlpatterns += patterns('taxon_home.views.applications.registered',
    #url(r'^images/editor/submit/$', 'SubmitImageTag.Application.renderAction'),
    url(r'^administration/$', 'Administration.Application.renderAction'),
    #url(r'^administration/gbrowse_manager/$', 'mycoplasma_home.views.gbrowse_manager'),
    #url(r'^administration/gbrowse_manager/genome_uploader/$', 'mycoplasma_home.views.genome_uploader'),
    url(r'^administration/imageManager/$', 'ImageManager.Application.renderAction'),
    url(r'^administration/deleteImage$', 'DeleteImage.Application.renderAction'),
    url(r'^administration/imageManager/getSlider$', 'ImageSlider.Application.renderAction'),
    url(r'^administration/addNewTagGroup$', 'AddNewTagGroup.Application.renderAction'),
    url(r'^administration/saveTag$','SaveTag.Application.renderAction'),
    url(r'^administration/addNewGeneLink$','AddNewGeneLink.Application.renderAction')
)
'''
urlpatterns += patterns('taxon_home.views.applications.admin',
    # admin patterns for urls
)
'''

urlpatterns += patterns('', 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static_site/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATICFILES_DIRS[0]}),
    url(r'^static/admin/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/usr/local/lib/python2.6/dist-packages/django/contrib/admin/media'}),
    url(r'^uploader/', include('BioDIG.multiuploader.urls'), name='main')
)
