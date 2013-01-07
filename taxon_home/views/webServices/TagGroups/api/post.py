import taxon_home.views.util.ErrorConstants as Errors
from taxon_home.models import Picture, TagGroup
from django.core.exceptions import ObjectDoesNotExist
from renderEngine.WebServiceObject import WebServiceObject
from django.db import transaction, DatabaseError

class PostAPI:
    
    def __init__(self, user, fields=None):
        self.user = user
        self.fields = fields
        
    '''
        Creates a new tag with the given parameters
        
        @param points: The points for a tag in an array of dictionaries
            format: [{"x" : 256, "y" : 350}, ...]
        @param description: The description for this tag
        @param color: The color array for this tag
            format: [r, g, b]
    '''    
    def createTagGroup(self, imageKey, name, isKey=True):
        metadata = WebServiceObject()
        
        try:
            if isKey:
                image = Picture.objects.get(pk__exact=imageKey)
            else:
                image = imageKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_TAG_GROUP_KEY
            
        authenticated = True
        if self.user and self.user.is_authenticated():
            authenticated = image.user == self.user or self.user.is_staff
        
        if not authenticated:
            raise Errors.AUTHENTICATION
        
        # start saving the new tag now that it has passed all tests
        tagGroup = TagGroup(name=name, picture=image)
        try:
            tagGroup.save()
        except DatabaseError as e:
            transaction.rollback()
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))
        # limit metadata return
        metadata.limitFields(self.fields)
        
        # add new tag to response for success
        metadata.put('id', tagGroup.pk)
        metadata.put('name', tagGroup.name)
        metadata.put('dateCreated', tagGroup.dateCreated.strftime("%Y-%m-%d %H:%M:%S"))
        metadata.put('lastModified', tagGroup.lastModified.strftime("%Y-%m-%d %H:%M:%S"))
        metadata.put('imageId', tagGroup.picture.pk)
        
        return metadata
        
        