import base.util.ErrorConstants as Errors
from base.models import Tag
from django.core.exceptions import ObjectDoesNotExist
from renderEngine.WebServiceObject import WebServiceObject
from django.db import transaction, DatabaseError

class PutAPI:
    
    def __init__(self, user=None, fields=None):
        self.user = user
        self.fields = fields
        
    '''
        Updates the given key with the update parameters
        
        @param tagKey: The tag's key to update or the tag itself
        @param updateParams: A dictionary of the new parameters for the tag to be changed
        @isKey: Indicates whether the input tagKey is actually a key or not
    '''
    @transaction.commit_on_success 
    def updateTag(self, tagKey, name=None, isKey=True):
        metadata = WebServiceObject()
        try:
            if (isKey):
                tag = Tag.objects.get(pk__exact=tagKey)
            else:
                tag = tagKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_TAG_GROUP_KEY
        
        if not tag.writePermissions(self.user):
            raise Errors.AUTHENTICATION
        
        # update the name
        if name:
            tag.name = name
        
        metadata.limitFields(self.fields)
        try:
            tag.save()
        except DatabaseError as e:
            transaction.rollback()
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))
        
        # add new tag to response for success
        metadata.put('name', tag.name)
        metadata.put('color', tag.color)
        metadata.put('group', tag.group)
        metadata.put('dateCreated', tag.dateCreated.strftime("%Y-%m-%d %H:%M:%S"))
        metadata.put('lastModified', tag.lastModified.strftime("%Y-%m-%d %H:%M:%S"))
        metadata.put('user', tag.user)
        metadata.put('isPrivate', tag.isPrivate)
        
        return metadata
