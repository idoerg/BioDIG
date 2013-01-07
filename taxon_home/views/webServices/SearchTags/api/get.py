import taxon_home.views.util.ErrorConstants as Errors
from taxon_home.models import TagGroup, Tag, TagPoint, Picture
from django.core.exceptions import ObjectDoesNotExist
from renderEngine.WebServiceObject import WebServiceArray, LimitDict

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
            if (isKey):
                tagGroup = TagGroup.objects.get(pk__exact=tagGroupKey)
            else:
                tagGroup = tagGroupKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_TAG_GROUP_KEY
            
        authenticated = True
        
        if tagGroup.picture.isPrivate:
            if self.user and self.user.is_authenticated():
                authenticated = tagGroup.picture.user == self.user
            else:
                authenticated = False
                
        if not authenticated:
            raise Errors.AUTHENTICATION
        
        if (self.unlimited):
            tags = Tag.objects.filter(group__exact=tagGroup).order_by('pk')[self.offset:]
        else:
            tags = Tag.objects.filter(group__exact=tagGroup).order_by('pk')[self.offset : self.offset+self.limit]
        
        for tag in tags:
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
                    'color' : color,
                    'points' : points,
                    'description' : tag.description
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
            if (isKey):
                image = Picture.objects.get(pk__exact=imageKey)
            else:
                image =imageKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_IMAGE_KEY
            
        authenticated = True
        
        if (image.isPrivate):
            if (self.user and self.user.is_authenticated()):
                authenticated = image.user == self.user
            else:
                authenticated = False
                
        if not authenticated:
            raise Errors.AUTHENTICATION
        
        tagGroups = TagGroup.objects.filter(picture__exact=image)
        
        if (self.unlimited):
            tags = Tag.objects.filter(group__in=tagGroups).order_by('pk')[self.offset:]
        else:
            tags = Tag.objects.filter(group__in=tagGroups).order_by('pk')[self.offset : self.offset+self.limit]
        
        for tag in tags:
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
                    'color' : color,
                    'points' : points,
                    'description' : tag.description
                })
            )
            
        return metadata

    
    '''
        Gets all the tags in the database that are private
    '''
    def getTags(self):
        metadata = WebServiceArray()
          
        if (self.user and self.user.is_authenticated()):
            images = Picture.objects.filter(isPrivate=False) | Picture.objects.filter(user__exact=self.user, isPrivate=True)
            
        else:
            images = Picture.objects.filter(isPrivate=False)
            
        tagGroups = TagGroup.objects.filter(picture__in=images)
                
        if (self.unlimited):
            tags = Tag.objects.filter(group__in=tagGroups).order_by('pk')[self.offset:]
        else:
            tags = Tag.objects.filter(group__in=tagGroups).order_by('pk')[self.offset : self.offset+self.limit]
        
        for tag in tags:
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
                    'color' : color,
                    'points' : points,
                    'description' : tag.description
                })
            )
                 
        return metadata 