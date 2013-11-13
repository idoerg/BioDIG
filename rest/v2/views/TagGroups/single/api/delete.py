import base.util.ErrorConstants as Errors
from base.models import TagGroup
from django.core.exceptions import ObjectDoesNotExist
from base.renderEngine.WebServiceObject import WebServiceObject, LimitDict
from django.db import transaction, DatabaseError
from base.serializers import TagGroupSerializer

class DeleteAPI:
    
    def __init__(self, user=None, fields=None):
        self.user = user
        self.fields = fields
    
    '''
        Gets all the tags in the database that are private
    '''
    @transaction.commit_on_success 
    def deleteTagGroup(self, tagGroupKey, isKey=True):
        metadata = WebServiceObject()
        
        try:
            if isKey:
                tagGroup = TagGroup.objects.get(pk__exact=tagGroupKey)
            else:
                tagGroup = tagGroupKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_TAG_GROUP_KEY
        except Exception:
            raise Errors.INTERNAL_ERROR
        
        if not tagGroup.writePermissions(self.user):
            raise Errors.AUTHENTICATION
       
        metadata.setObject(LimitDict(self.fields, TagGroupSerializer(tagGroup).data))

        try:
            tagGroup.delete()
        except DatabaseError as e:
            transaction.rollback()
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))
        
        return metadata
