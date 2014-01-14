import base.util.ErrorConstants as Errors
from base.models import Organism
from django.core.exceptions import ObjectDoesNotExist
from renderEngine.WebServiceObject import WebServiceObject
from django.db import transaction, DatabaseError

class PutAPI:
    
    def __init__(self, user=None, fields=None):
        self.user = user
        self.fields = fields
        
    '''
        Updates the given key with the update parameters
        
        @param organismKey: The tag's key to update or the tag itself
        @param updateParams: A dictionary of the new parameters for the tag to be changed
        @isKey: Indicates whether the input tagKey is actually a key or not
    '''
    @transaction.commit_on_success 
    def updateOrganism(self, organismKey, name=None, isKey=True):
        metadata = WebServiceObject()
        try:
            if (isKey):
                organism = Organism.objects.get(pk__exact=organismKey)
            else:
                organism = organismKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_TAG_GROUP_KEY
        
        if not organism.writePermissions(self.user):
            raise Errors.AUTHENTICATION
        
        # update the name
        if name:
            organism.name = name
        
        metadata.limitFields(self.fields)
        try:
            organism.save()
        except DatabaseError as e:
            transaction.rollback()
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))
        
        # add new tag to response for success
        metadata.put('organism_id', organism.pk)
        metadata.put('abbreviation', organism.abbreviation)
        metadata.put('genus', organism.genus)
        metadata.put('species', organism.species)
        metadata.put('common_name', organism.name)
        metadata.put('comment', organism.comment)
        
        return metadata
