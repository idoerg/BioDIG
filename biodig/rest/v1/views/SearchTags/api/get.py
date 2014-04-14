import biodig.base.util.ErrorConstants as Errors
from biodig.base.models import TagGroup, Tag, TagPoint, Image
from django.core.exceptions import ObjectDoesNotExist
from biodig.base.renderEngine.WebServiceObject import WebServiceArray, LimitDict

class GetAPI:
    
    def __init__(self, limit=10, offset=0, user=None, fields=None, unlimited=False):
        self.limit = limit
        self.offset = offset
        self.unlimited = unlimited
        self.user = user
        self.fields = fields

    '''
        Gets the tags associated with the given tag group
        
        @param tagGroupKey: The primary key for the tag group or the tag group
    '''
    def getTagsByTagGroup(self, tagGroupKey, isKey=True):
        metadata = WebServiceArray()
        
        try:
            if isKey:
                tagGroup = TagGroup.objects.get(pk__exact=tagGroupKey)
            else:
                tagGroup = tagGroupKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_TAG_GROUP_KEY
            
        if not tagGroup.readPermissions(self.user):
            raise Errors.AUTHENTICATION
        
        if self.unlimited:
            tags = Tag.objects.filter(group__exact=tagGroup).order_by('pk')[self.offset:]
        else:
            tags = Tag.objects.filter(group__exact=tagGroup).order_by('pk')[self.offset : self.offset+self.limit]
        
        for tag in tags:
            if tag.readPermissions(self.user):
                tagPoints = TagPoint.objects.filter(tag__exact = tag).order_by('rank')
                points = []
                
                for tagPoint in tagPoints:
                    points.append({
                        'x' : tagPoint.pointX, 
                        'y' : tagPoint.pointY
                    })
                
                color = [tag.color.red, tag.color.green, tag.color.blue]
                
                metadata.put(
                    LimitDict(self.fields, {
                        'id' : tag.pk,
                        'user' : tag.user.username,
                        'color' : color,
                        'points' : points,
                        'name' : tag.name
                    })
                )

        return metadata
    
    '''
        Gets the tags associated with the given image
        
        @param imageKey: The primary key for the image or the image
    ''' 
    def getTagsByImage(self, imageKey, isKey=True):
        metadata = WebServiceArray()
        
        try:
            if isKey:
                image = Image.objects.get(pk__exact=imageKey)
            else:
                image =imageKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_IMAGE_KEY

        if not image.readPermissions(self.user):
            raise Errors.AUTHENTICATION
        
        tagGroups = TagGroup.objects.filter(picture__exact=image)
        
        if self.unlimited:
            tags = Tag.objects.filter(group__in=tagGroups).order_by('pk')[self.offset:]
        else:
            tags = Tag.objects.filter(group__in=tagGroups).order_by('pk')[self.offset : self.offset+self.limit]
        
        for tag in tags:
            if tag.readPermissions(self.user):
                tagPoints = TagPoint.objects.filter(tag__exact = tag).order_by('rank')
                points = []
                
                for tagPoint in tagPoints:
                    points.append([
                        tagPoint.pointX, 
                        tagPoint.pointY
                    ])
                
                color = [tag.color.red, tag.color.green, tag.color.blue]
                
                metadata.put(
                    LimitDict(self.fields, {
                        'id' : tag.pk,
                        'user' : tag.user.username,
                        'color' : color,
                        'points' : points,
                        'name' : tag.name
                    })
                )
            
        return metadata

    
    '''
        Gets all the tags in the database that are private
    '''
    def getTags(self):
        metadata = WebServiceArray()
          
        if (self.user and self.user.is_authenticated()):
            images = Image.objects.filter(isPrivate=False) | Image.objects.filter(user__exact=self.user, isPrivate=True)
            
        else:
            images = Image.objects.filter(isPrivate=False)
        
        tagGroups = TagGroup.objects.filter(picture__in=images)
                
        if (self.unlimited):
            tags = Tag.objects.filter(group__in=tagGroups).order_by('pk')[self.offset:]
        else:
            tags = Tag.objects.filter(group__in=tagGroups).order_by('pk')[self.offset : self.offset+self.limit]
        
        for tag in tags:
            if tag.readPermissions(self.user):
                tagPoints = TagPoint.objects.filter(tag__exact = tag).order_by('rank')
                points = []
                
                for tagPoint in tagPoints:
                    points.append([
                        tagPoint.pointX, 
                        tagPoint.pointY
                    ])
                
                color = [tag.color.red, tag.color.green, tag.color.blue]
                
                metadata.put(
                    LimitDict(self.fields, {
                        'id' : tag.pk,
                        'user' : tag.user.username,
                        'color' : color,
                        'points' : points,
                        'name' : tag.name
                    })
                )
                 
        return metadata 
