from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

urlpatterns = patterns('services.views',
    url(r'^tags$', 'Tags.Application.renderAction'),
    url(r'^tagGroups$', 'TagGroups.Application.renderAction'),
    url(r'^geneLinks$', 'GeneLinks.Application.renderAction'),
    url(r'^images$', 'Images.Application.renderAction'),
    url(r'^geneLinks/search$', 'SearchGeneLinks.Application.renderAction'),
    url(r'^tags/search$', 'SearchTags.Application.renderAction'),
    url(r'^tagGroups/search$', 'SearchTagGroups.Application.renderAction'),
    url(r'^aggregate/tagGroups$', 'AggregateTagGroups.Application.renderAction'),
    url(r'^aggregate/tagGroups/search$', 'AggregateTagGroupsSearch.Application.renderAction'),
    url(r'^images/search$', 'SearchImages.Application.renderAction'),
    url(r'^organisms/search$', 'SearchOrganisms.Application.renderAction')
)
