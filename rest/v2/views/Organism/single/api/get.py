import base.util.ErrorConstants as Errors
from base.models import Organism
from django.core.exceptions import ObjectDoesNotExist
from renderEngine.WebServiceObject import WebServiceObject

class GetAPI:
    
    def __init__(self, user=None, fields=None):
        self.user = user
        self.fields = fields
    
    '''
        Gets all the Organisms in the database that are private
    '''
    def getOrganism(self, organismKey, isKey=True):
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
        
        if not organism.readPermissions(self.user):
            raise Errors.AUTHENTICATION

        metadata.limitFields(self.fields)
                
        metadata.put('organism_id', organism.pk)
        metadata.put('abbreviation', organism.abbreviation)
        metadata.put('genus', organism.genus)
        metadata.put('species', organism.species)
        metadata.put('common_name', organism.name)
        metadata.put('comment', organism.comment)
        
        return metadata
