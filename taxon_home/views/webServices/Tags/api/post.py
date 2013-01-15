import taxon_home.views.util.ErrorConstants as Errors
from taxon_home.models import Tag, TagPoint, TagColor, TagGroup
from django.core.exceptions import ObjectDoesNotExist
from renderEngine.WebServiceObject import WebServiceObject
from django.db import transaction, DatabaseError

class PostAPI:
    
    def __init__(self, user, fields=None):
        self.user = user
        self.fields = fields
        
    '''
        Creates a new tag with the given parameters
        
        @param points: The points for a tag in an array of dictionaries
            format: [{"x" : 256, "y" : 350}, ...]
        @param description: The description for this tag
        @param color: The color array for this tag
            format: [r, g, b]
    '''   
    @transaction.commit_on_success  
    def createTag(self, tagGroupKey, points, description, color, isKey=True):
        metadata = WebServiceObject()
        tagPoints = []
        
        try:
            if isKey:
                tagGroup = TagGroup.objects.get(pk__exact=tagGroupKey)
            else:
                tagGroup = tagGroupKey
        except (ObjectDoesNotExist, ValueError):
                raise Errors.INVALID_TAG_GROUP_KEY
            
        authenticated = True
        if self.user and self.user.is_authenticated():
            authenticated = tagGroup.picture.user == self.user or self.user.is_staff
        
        if not authenticated:
            raise Errors.AUTHENTICATION
            
        # create the new tag points to put in the tag
        try:
            for counter, point in enumerate(points):
                tagPoints.append(TagPoint(pointX=float(point['x']), pointY=float(point['y']) , rank=counter+1))
        except (TypeError, KeyError, ValueError):
            raise Errors.INVALID_SYNTAX.setCustom('points')
        
        try:
            # create new tag color
            try:
                if len(color) == 3:
                    tagColor = TagColor.objects.get_or_create(red=int(color[0]), green=int(color[1]), blue=int(color[2]))[0]
            except (ValueError, TypeError):
                raise Errors.INVALID_SYNTAX.setCustom('color')
            
            # start saving the new tag now that it has passed all tests
            tag = Tag(description=description, color=tagColor, group=tagGroup)
            tag.save()
            
            for tagPoint in tagPoints:
                tagPoint.tag = tag
                tagPoint.save()
        except DatabaseError as e:
            transaction.rollback()
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))
        
        # limit metadata return
        metadata.limitFields(self.fields)
        
        # add new tag to response for success
        metadata.put('id', tag.pk)
        metadata.put('color', [tag.color.red, tag.color.green, tag.color.blue])
        metadata.put('description', tag.description)
        metadata.put('points', points)
        
        return metadata
        
        