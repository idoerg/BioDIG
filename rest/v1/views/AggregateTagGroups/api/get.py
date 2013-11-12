import base.util.ErrorConstants as Errors
from base.models import TagGroup
from base.renderEngine.WebServiceObject import WebServiceObject
from django.core.exceptions import ObjectDoesNotExist
from services.views.SearchGeneLinks.api.get import GetAPI as GeneLinkAPI
from services.views.SearchTags.api.get import GetAPI as TagAPI
from services.views.TagGroups.api.get import GetAPI as TagGroupAPI


class GetAPI:
    
    def __init__(self, user=None, fields=None, unlimited=False):
        self.unlimited = unlimited
        self.user = user
        self.fields = fields
        
    '''
        Gets the tag group
        
        @param imageKey: The primary key for the tag group or the tag group
        @param isKey: Whether the first argument is a key object or not (default: true)
    '''
    def getTagGroup(self, tagGroupKey, isKey=True):
        metadata = WebServiceObject()
        
        try:
            if isKey:
                group = TagGroup.objects.get(pk__exact=tagGroupKey)
            else:
                group = tagGroupKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_TAG_GROUP_KEY
                
        # initialize tagging APIs
        tagGroupAPI = TagGroupAPI(self.user, self.fields)
        tagAPI = TagAPI(user=self.user, unlimited=True)
        geneLinkAPI = GeneLinkAPI(user=self.user, unlimited=True)
        
        group = tagGroupAPI.getTagGroup(group, isKey=False).getObject()

        tags = tagAPI.getTagsByTagGroup(group['id']).getObject()
        for tag in tags:
            geneLinks = geneLinkAPI.getGeneLinksByTag(tag['id']).getObject()
            tag['geneLinks'] = geneLinks
        group['tags'] = tags
            
        metadata.setObject(group)
    
        return metadata
