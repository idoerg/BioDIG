from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('web.public.views.applications',
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
    url(r'^search/$', 'Search.Application.renderAction'),
    url(r'^advancedSearch/$', 'AdvancedSearch.Application.renderAction')
)
