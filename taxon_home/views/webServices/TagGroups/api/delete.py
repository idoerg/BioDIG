import taxon_home.views.util.ErrorConstants as Errors
from taxon_home.models import TagGroup
from django.core.exceptions import ObjectDoesNotExist
from renderEngine.WebServiceObject import WebServiceObject
from django.db import transaction, DatabaseError

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
            if (isKey):
                tagGroup = TagGroup.objects.get(pk__exact=tagGroupKey)
            else:
                tagGroup = tagGroupKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_TAG_GROUP_KEY
        except Exception:
            raise Errors.INTERNAL_ERROR
        
        metadata.limitFields(self.fields)
                
        # add new tag to response for success
        metadata.put('id', tagGroup.pk)
        metadata.put('name', tagGroup.name)
        metadata.put('dateCreated', tagGroup.dateCreated.strftime("%Y-%m-%d %H:%M:%S"))
        metadata.put('lastModified', tagGroup.lastModified.strftime("%Y-%m-%d %H:%M:%S"))
        metadata.put('imageId', tagGroup.picture.pk)
        
        try:
            tagGroup.delete()
        except DatabaseError as e:
            transaction.rollback()
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))
        
        return metadata