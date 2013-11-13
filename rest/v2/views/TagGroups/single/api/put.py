import base.util.ErrorConstants as Errors
from base.models import TagGroup
from django.core.exceptions import ObjectDoesNotExist
from base.renderEngine.WebServiceObject import WebServiceObject, LimitDict
from django.db import transaction, DatabaseError
from base.serializers import TagGroupSerializer

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
        
        try:
            tagGroup.save()
        except DatabaseError as e:
            transaction.rollback()
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))
        
        metadata.setObject(LimitDict(self.fields, TagGroupSerializer(tagGroup).data))
        return metadata
