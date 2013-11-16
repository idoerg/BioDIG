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
    def createTag(self, name, isKey=True):
        metadata = WebServiceObject()
        
        # start saving the new tag now that it has passed all tests
        tag = Tag(name=name, user=self.user)
        try:
            tag.save()
        except DatabaseError as e:
            transaction.rollback()
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))
        # limit metadata return
        metadata.limitFields(self.fields)
        
        # add new tag to response for success
        metadata.put('id', tag.pk)
        metadata.put('name', tag.name)
        metadata.put('user', tag.user.username)
        metadata.put('dateCreated', tag.dateCreated.strftime("%Y-%m-%d %H:%M:%S"))
        metadata.put('lastModified', tag.lastModified.strftime("%Y-%m-%d %H:%M:%S"))
        metadata.put('image', tag.picture.pk)
        metadata.put('isPrivate', tag.isPrivate)
        
        return metadata
        
        
