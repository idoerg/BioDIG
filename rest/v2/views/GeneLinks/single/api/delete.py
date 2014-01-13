import base.util.ErrorConstants as Errors
from base.models import GeneLink
from django.core.exceptions import ObjectDoesNotExist
from renderEngine.WebServiceObject import WebServiceObject
from django.db import transaction, DatabaseError

class DeleteAPI:
    
    def __init__(self, user=None, fields=None):
        self.user = user
        self.fields = fields
    
    '''
        Gets all the geneLinks in the database that are private
    '''
    @transaction.commit_on_success 
    def deleteGeneLink(self, geneLinkKey, isKey=True):
        metadata = WebServiceObject()
        
        try:
            if (isKey):
                geneLink = GeneLink.objects.get(pk__exact=geneLinkKey)
            else:
                geneLink = geneLinkKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_TAG_GROUP_KEY
        except Exception:
            raise Errors.INTERNAL_ERROR
        
        if not geneLink.writePermissions(self.user):
            raise Errors.AUTHENTICATION
        
        metadata.limitFields(self.fields)
                
        # add new tag to response for success
        metadata.put('tag', geneLink.pk)
        metadata.put('feature', geneLink.feature)
        metadata.put('dateCreated', geneLink.dateCreated.strftime("%Y-%m-%d %H:%M:%S"))
        metadata.put('lastModified', geneLink.lastModified.strftime("%Y-%m-%d %H:%M:%S"))
        metadata.put('user', geneLink.user)
        metadata.put('isPrivate', geneLink.isPrivate)
        
        try:
            geneLink.delete()
        except DatabaseError as e:
            transaction.rollback()
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))
        
        return metadata
