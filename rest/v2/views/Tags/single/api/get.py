import taxon_home.views.util.ErrorConstants as Errors
from taxon_home.models import Tag, TagPoint
from django.core.exceptions import ObjectDoesNotExist
from renderEngine.WebServiceObject import WebServiceObject

class GetAPI:
    
    def __init__(self, user=None, fields=None):
        self.user = user
        self.fields = fields
    
    '''
        Gets all the tags in the database that are private
    '''
    def getTag(self, tagKey, isKey=True):
        metadata = WebServiceObject()
        
        try:            
            if (isKey):
                tag = Tag.objects.get(pk__exact=tagKey)
            else:
                tag = tagKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_TAG_KEY
        except Exception:
            raise Errors.INTERNAL_ERROR
            
        if not tag.readPermissions(self.user):
            raise Errors.AUTHENTICATION
        
        metadata.limitFields(self.fields)
        
        if metadata.allowsField('points'):
            tagPoints = TagPoint.objects.filter(tag__exact=tag)
            
            points = []
            
            for tagPoint in tagPoints:
                points.append({
                    'x' : tagPoint.pointX, 
                    'y' : tagPoint.pointY
                })
            
            metadata.put('points', points)
        
        metadata.put('id', tag.pk)
        metadata.put('color', [tag.color.red, tag.color.green, tag.color.blue])
        metadata.put('name', tag.name)
        
        return metadata