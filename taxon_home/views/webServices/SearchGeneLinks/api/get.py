import taxon_home.views.util.ErrorConstants as Errors
from taxon_home.models import GeneLink, Tag, TagGroup, Picture
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
        Gets the gene links registered to the tag key provided
        
        @param tagKey: Key or tag object used to retrieve the gene links
    '''        
    def getGeneLinksByTag(self, tagKey, isKey=True):
        metadata = WebServiceArray()
        
        try:
            if (isKey):
                tag = Tag.objects.get(pk__exact=tagKey)
            else:
                tag = tagKey
            
            authenticated = True
            
            if (tag.group.picture.isPrivate):
                if (self.user and self.user.is_authenticated()):
                    authenticated = tag.group.picture.user == self.user
                else:
                    authenticated = False
                    
            if (authenticated):
                
                if (self.unlimited):
                    geneLinks = GeneLink.objects.filter(tag__exact=tag).order_by('pk')[self.offset:]
                else:
                    geneLinks = GeneLink.objects.filter(tag__exact=tag).order_by('pk')[self.offset : self.offset+self.limit]
                                
                for geneLink in geneLinks:
                    metadata.put(
                        LimitDict(self.fields, {
                            'id' : geneLink.pk,
                            'tagId' : tag.pk,
                            'uniquename' : geneLink.feature.uniquename,
                            'name' : geneLink.feature.name,
                            'organismId' : geneLink.feature.organism.organism_id,
                        })    
                    )
            else:
                metadata.setError(Errors.AUTHENTICATION)
        except ObjectDoesNotExist:
            metadata.setError(Errors.INVALID_TAG_KEY)
        
        return metadata
    
    '''
        Gets the gene links registered to the tag group key provided
        
        @param tagGroupKey: Key or tagGroup object used to retrieve the gene links
    '''        
    def getGeneLinksByTagGroup(self, tagGroupKey, isKey=True):
        metadata = WebServiceArray()
        
        try:
            if (isKey):
                tagGroup = TagGroup.objects.get(pk__exact=tagGroupKey)
            else:
                tagGroup = tagGroupKey
            
            authenticated = True
            
            if (tagGroup.picture.isPrivate):
                if (self.user and self.user.is_authenticated()):
                    authenticated = tagGroup.picture.user == self.user
                else:
                    authenticated = False
                    
            if (authenticated):
                
                tags = Tag.objects.filter(group__exact=tagGroup)
                
                if (self.unlimited):
                    geneLinks = GeneLink.objects.filter(tag__in=tags).order_by('pk')[self.offset:]
                else:
                    geneLinks = GeneLink.objects.filter(tag__in=tags).order_by('pk')[self.offset : self.offset+self.limit]
                    
                for geneLink in geneLinks:
                    metadata.put(
                        LimitDict(self.fields, {
                            'id' : geneLink.pk,
                            'tagId' : geneLink.tag.pk,
                            'uniquename' : geneLink.feature.uniquename,
                            'name' : geneLink.feature.name,
                            'organismId' : geneLink.feature.organism.organism_id,
                        })    
                    )
            else:
                metadata.setError(Errors.AUTHENTICATION)
        except ObjectDoesNotExist:
            metadata.setError(Errors.INVALID_TAG_KEY)
        
        return metadata
    
    '''
        Gets the gene links registered to the image key provided
        
        @param imageKey: Key or image object used to retrieve the gene links
    '''        
    def getGeneLinksByImage(self, imageKey, isKey=True):
        metadata = WebServiceArray()
        
        try:
            if (isKey):
                image = TagGroup.objects.get(pk__exact=imageKey)
            else:
                image = imageKey
            
            authenticated = True
            
            if (image.isPrivate):
                if (self.user and self.user.is_authenticated()):
                    authenticated = image.user == self.user
                else:
                    authenticated = False
                    
            if (authenticated):
                
                tagGroups = TagGroup.objects.filter(picture__exact=image)
                
                tags = Tag.objects.filter(group__in=tagGroups)
                
                if (self.unlimited):
                    geneLinks = GeneLink.objects.filter(tag__in=tags).order_by('pk')[self.offset:]
                else:
                    geneLinks = GeneLink.objects.filter(tag__in=tags).order_by('pk')[self.offset : self.offset+self.limit]
                
                for geneLink in geneLinks:
                    metadata.put(
                        LimitDict(self.fields, {
                            'id' : geneLink.pk,
                            'tagId' : geneLink.tag.pk,
                            'uniquename' : geneLink.feature.uniquename,
                            'name' : geneLink.feature.name,
                            'organismId' : geneLink.feature.organism.organism_id
                        })    
                    )
            else:
                metadata.setError(Errors.AUTHENTICATION)
        except ObjectDoesNotExist:
            metadata.setError(Errors.INVALID_TAG_KEY)
        
        return metadata
    
    '''
        Gets all the gene links
    '''        
    def getGeneLinks(self):
        metadata = WebServiceArray()
        
        try:
            if (self.user and self.user.is_authenticated()):
                images = Picture.objects.filter(isPrivate=False) | Picture.objects.filter(user__exact=self.user, isPrivate=True)
            else:
                images = Picture.objects.filter(isPrivate=False)
                
            tagGroups = TagGroup.objects.filter(picture__in=images)
                    
            tags = Tag.objects.filter(group__in=tagGroups)
                    
            if (self.unlimited):
                geneLinks = GeneLink.objects.filter(tag__in=tags).order_by('pk')[self.offset:]
            else:
                geneLinks = GeneLink.objects.filter(tag__in=tags).order_by('pk')[self.offset : self.offset+self.limit]
            
            for geneLink in geneLinks:
                metadata.put(
                    LimitDict(self.fields, {
                        'id' : geneLink.pk,
                        'tagId' : geneLink.tag.pk,
                        'uniquename' : geneLink.feature.uniquename,
                        'name' : geneLink.feature.name,
                        'organismId' : geneLink.feature.organism.organism_id
                    })
                )
        except ValueError:
            metadata.setError(Errors.INVALID_TAG_GROUP_KEY)    
            
        return metadata
        
        
        
        