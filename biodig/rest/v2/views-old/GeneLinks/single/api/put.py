import base.util.ErrorConstants as Errors
from base.models import GeneLink
from django.core.exceptions import ObjectDoesNotExist
from renderEngine.WebServiceObject import WebServiceObject
from django.db import transaction, DatabaseError

class PutAPI:
    
    def __init__(self, user=None, fields=None):
        self.user = user
        self.fields = fields
        
    '''
        Updates the given key with the update parameters
        
        @param geneLinkKey: The tag's key to update or the tag itself
        @param updateParams: A dictionary of the new parameters for the tag to be changed
        @isKey: Indicates whether the input tagKey is actually a key or not
    '''
    @transaction.commit_on_success 
    def updateGeneLink(self, geneLinkKey, name=None, isKey=True):
        metadata = WebServiceObject()
        try:
            if (isKey):
                geneLink = GeneLink.objects.get(pk__exact=geneLinkKey)
            else:
                geneLink = geneLinkKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_TAG_GROUP_KEY
        
        if not geneLink.writePermissions(self.user):
            raise Errors.AUTHENTICATION
        
        # update the name
        if name:
            geneLink.name = name
        
        metadata.limitFields(self.fields)
        try:
            geneLink.save()
        except DatabaseError as e:
            transaction.rollback()
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))
        
        # add new tag to response for success
        metadata.put('tag', geneLink.pk)
        metadata.put('feature', geneLink.feature)
        metadata.put('dateCreated', geneLink.dateCreated.strftime("%Y-%m-%d %H:%M:%S"))
        metadata.put('lastModified', geneLink.lastModified.strftime("%Y-%m-%d %H:%M:%S"))
        metadata.put('user', geneLink.user)
        metadata.put('isPrivate', geneLink.isPrivate)
        
        return metadata
