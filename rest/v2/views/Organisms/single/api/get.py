import taxon_home.views.util.ErrorConstants as Errors
from taxon_home.models import Organism
from django.core.exceptions import ObjectDoesNotExist
from renderEngine.WebServiceObject import WebServiceObject

class GetAPI:
    
    def __init__(self, user=None, fields=None):
        self.user = user
        self.fields = fields
    
    '''
        Gets all the tags in the database that are private
    '''
    def getOrganism(self, organismKey, isKey=True):
        metadata = WebServiceObject()
        
        try:            
            if (isKey):
                organism = Organism.objects.get(pk__exact=organismKey)
            else:
                organism = organismKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_PARAMETER('id')
        except Exception:
            raise Errors.INTERNAL_ERROR

        metadata.limitFields(self.fields)
                
        metadata.put('id', organism.organism_id)
        metadata.put('abbreviation', organism.abbreviation)
        metadata.put('genus', organism.genus)
        metadata.put('species', organism.species)
        metadata.put('commonName', organism.common_name)
        metadata.put('comment', organism.comment)
        
        return metadata