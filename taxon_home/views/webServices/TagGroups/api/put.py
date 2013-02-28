import taxon_home.views.util.ErrorConstants as Errors
from taxon_home.models import TagGroup
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
    def updateTagGroup(self, tagGroupKey, name=None, isKey=True):
        metadata = WebServiceObject()
        try:
            if (isKey):
                tagGroup = TagGroup.objects.get(pk__exact=tagGroupKey)
            else:
                tagGroup = tagGroupKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_TAG_GROUP_KEY
        
        if not tagGroup.writePermissions(self.user):
            raise Errors.AUTHENTICATION
        
        # update the name
        if name:
            tagGroup.name = name
        
        metadata.limitFields(self.fields)
        try:
            tagGroup.save()
        except DatabaseError as e:
            transaction.rollback()
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))
        
        # add new tag to response for success
        metadata.put('id', tagGroup.pk)
        metadata.put('name', tagGroup.name)
        metadata.put('user', tagGroup.user.username)
        metadata.put('dateCreated', tagGroup.dateCreated.strftime("%Y-%m-%d %H:%M:%S"))
        metadata.put('lastModified', tagGroup.lastModified.strftime("%Y-%m-%d %H:%M:%S"))
        metadata.put('imageId', tagGroup.picture.pk)
        metadata.put('isPrivate', tagGroup.isPrivate)
        
        return metadata