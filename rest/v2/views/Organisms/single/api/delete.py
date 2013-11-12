import taxon_home.views.util.ErrorConstants as Errors
from taxon_home.models import Organism
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
    def deleteOrganism(self, organismKey, isKey=True):
        metadata = WebServiceObject()
        
        try:
            if (isKey):
                organism = Organism.objects.get(pk__exact=organismKey)
            else:
                organism = organismKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_TAG_GROUP_KEY
        except Exception:
            raise Errors.INTERNAL_ERROR
        
        if not organism.writePermissions(self.user):
            raise Errors.AUTHENTICATION
        
        metadata.limitFields(self.fields)
                
        # add new tag to response for success
        metadata.put('id', organism.organism_id)
        metadata.put('abbreviation', organism.abbreviation)
        metadata.put('genus', organism.genus)
        metadata.put('species', organism.species)
        metadata.put('commonName', organism.common_name)
        metadata.put('comment', organism.comment)
        
        try:
            organism.delete()
        except DatabaseError as e:
            transaction.rollback()
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))
        
        return metadata