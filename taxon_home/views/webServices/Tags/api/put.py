import taxon_home.views.util.ErrorConstants as Errors
from taxon_home.models import Tag, TagPoint, TagColor
from django.core.exceptions import ObjectDoesNotExist
from renderEngine.WebServiceObject import WebServiceObject
from django.db import transaction, DatabaseError

class PutAPI:
    
    def __init__(self, user=None, fields=None):
        self.user = user
        self.fields = fields
        
    '''
        Updates the given key with the update parameters
        
        @param tagKey: The tag's key to update or the tag itself
        @param updateParams: A dictionary of the new parameters for the tag to be changed
        @isKey: Indicates whether the input tagKey is actually a key or not
    '''    
    @transaction.commit_on_success 
    def updateTag(self, tagKey, points=None, description=None, color=None, isKey=True):
        metadata = WebServiceObject()
        try:
            if (isKey):
                tag = Tag.objects.get(pk__exact=tagKey)
            else:
                tag = tagKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_TAG_KEY
            
        
        authenticated = True
        
        if tag.group.picture.isPrivate:
            if self.user and self.user.is_authenticated():
                authenticated = tag.group.picture.user == self.user
            else:
                authenticated = False
        
        if not authenticated:
            raise Errors.AUTHENTICATION
        
        # update the description
        if description:
            tag.description = description
        
        # update the color (ignores bad syntax)
        try:
            if color and len(color) == 3:
                tagColor = TagColor.objects.get_or_create(red=color[0], green=color[1], blue=color[2])[0]
                tag.color = tagColor
        except (ValueError, TypeError):
            raise Errors.INVALID_SYNTAX.setCustom('color')
        
        oldTagPoints = list(TagPoint.objects.filter(tag__exact=tag))
        
        # updates the tag points for this tag
        if points:
            # first we delete the old tag points (they aren't helpful anymore)
            # TODO: add Trash database for restoring accidental changes                    
            try:
                newTagPointModels = []
                # Save the new tag points
                # create the new tag points to put in the tag
                for counter, point in enumerate(points):
                    newTagPointModels.append(TagPoint(pointX=float(point['x']), pointY=float(point['y']) , rank=counter+1))
                    
            except (TypeError, KeyError, ValueError):
                raise Errors.INVALID_SYNTAX.setCustom('points')
        
        metadata.limitFields(self.fields)
        try:
            tag.save()
            if points:
                for newTagPoint in newTagPointModels:
                    newTagPoint.tag = tag
                    newTagPoint.save()
                
                for tagPoint in oldTagPoints:
                    tagPoint.delete()
                
                metadata.put('points', points)
            else:
                tagPoints = []
                for tagPoint in oldTagPoints:
                    tagPoints.append({
                        'x' : tagPoint.pointX, 
                        'y' : tagPoint.pointY
                    })
                metadata.put('points', tagPoints)
        except DatabaseError as e:
            transaction.rollback()
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))
        
        # add new tag to response for success
        metadata.put('id', tag.pk)
        metadata.put('color', [tag.color.red, tag.color.green, tag.color.blue])
        metadata.put('description', tag.description)
        
        return metadata