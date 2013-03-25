import taxon_home.views.util.ErrorConstants as Errors
from taxon_home.models import Picture
from renderEngine.WebServiceObject import WebServiceArray
from django.core.exceptions import ObjectDoesNotExist
from taxon_home.views.webServices.SearchGeneLinks.api.get import GetAPI as GeneLinkAPI
from taxon_home.views.webServices.SearchTags.api.get import GetAPI as TagAPI
from taxon_home.views.webServices.SearchTagGroups.api.get import GetAPI as TagGroupAPI


class GetAPI:
    
    def __init__(self, limit=10, offset=0, user=None, fields=None, unlimited=False):
        self.limit = limit
        self.offset = offset
        self.unlimited = unlimited
        self.user = user
        self.fields = fields
        
    '''
        Gets the tag groups for the given image
        
        @param imageKey: The primary key for the image or the image
        @param isKey: Whether the first argument is a key object or not (default: true)
    '''
    def getAggregateTagGroupsByImage(self, imageKey, isKey=True):
        metadata = WebServiceArray()
        
        try:
            if (isKey):
                image = Picture.objects.get(pk__exact=imageKey)
            else:
                image = imageKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_IMAGE_KEY
                
        if not image.readPermissions(self.user):
            raise Errors.AUTHENTICATION
                
        # initialize tagging APIs
        tagGroupAPI = TagGroupAPI(self.limit, self.offset, self.user, self.fields, self.unlimited)
        tagAPI = TagAPI(user=self.user, unlimited=True)
        geneLinkAPI = GeneLinkAPI(user=self.user, unlimited=True)
        
        tagGroups = tagGroupAPI.getTagGroupsByImage(image, False).getObject()
        
        for group in tagGroups:
            tags = tagAPI.getTagsByTagGroup(group['id']).getObject()
            for tag in tags:
                geneLinks = geneLinkAPI.getGeneLinksByTag(tag['id']).getObject()
                tag['geneLinks'] = geneLinks
            group['tags'] = tags
            
        metadata.setObject(tagGroups)
    
        return metadata
    
    '''
        Gets the tag groups for the given image
        
        @param imageKey: The primary key for the image or the image
        @param isKey: Whether the first argument is a key object or not (default: true)
    '''
    def getAggregateTagGroups(self):
        metadata = WebServiceArray()
                
        # initialize tagging APIs
        tagGroupAPI = TagGroupAPI(self.limit, self.offset, self.user, self.fields, self.unlimited)
        tagAPI = TagAPI(user=self.user, unlimited=True)
        geneLinkAPI = GeneLinkAPI(user=self.user, unlimited=True)
        
        tagGroups = tagGroupAPI.getTagGroups().getObject()
        
        for group in tagGroups:
            tags = tagAPI.getTagsByTagGroup(group['id']).getObject()
            for tag in tags:
                geneLinks = geneLinkAPI.getGeneLinksByTag(tag['id']).getObject()
                tag['geneLinks'] = geneLinks
            group['tags'] = tags
            
        metadata.setObject(tagGroups)
    
        return metadata
