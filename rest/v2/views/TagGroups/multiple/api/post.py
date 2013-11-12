import base.util.ErrorConstants as Errors
from base.models import Picture, TagGroup
from django.core.exceptions import ObjectDoesNotExist
from base.renderEngine.WebServiceObject import WebServiceObject
from django.db import transaction, DatabaseError

class PostAPI:
    
    def __init__(self, user, fields=None):
        self.user = user
        self.fields = fields
        
    '''
        Creates a new tag with the given parameters
        
        @param imageKey: The key for the image to which this tag group belongs
        @param name: The description for this tag
    '''
    @transaction.commit_on_success 
    def createTagGroup(self, imageKey, name, isKey=True):
        metadata = WebServiceObject()
        
        try:
            if isKey:
                image = Picture.objects.get(pk__exact=imageKey)
            else:
                image = imageKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_IMAGE_KEY
        
        if not image.writePermissions(self.user):
            raise Errors.AUTHENTICATION
        
        # start saving the new tag now that it has passed all tests
        tagGroup = TagGroup(name=name, picture=image, user=self.user)
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
        metadata.put('user', tagGroup.user.username)
        metadata.put('dateCreated', tagGroup.dateCreated.strftime("%Y-%m-%d %H:%M:%S"))
        metadata.put('lastModified', tagGroup.lastModified.strftime("%Y-%m-%d %H:%M:%S"))
        metadata.put('image', tagGroup.picture.pk)
        metadata.put('isPrivate', tagGroup.isPrivate)
        
        return metadata
        
        
