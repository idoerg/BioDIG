import taxon_home.views.util.ErrorConstants as Errors
from taxon_home.models import Tag, GeneLink, Feature
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
    def createGeneLink(self, tagKey, name=None,  uniqueName=None, organismId=None, isKey=True):
        metadata = WebServiceObject()
        
        try:
            if isKey:
                tag = Tag.objects.get(pk__exact=tagKey)
            else:
                tag = tagKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_TAG_GROUP_KEY
            
        authenticated = True
        if self.user and self.user.is_authenticated():
            authenticated = tag.group.picture.user == self.user or self.user.is_staff
        
        if not authenticated:
            raise Errors.AUTHENTICATION 
        
        try:
            feature = None
            if name and organismId:
                feature = Feature.objects.filter(name=name, organism=organismId)
            if uniqueName:
                if feature:
                    feature = feature & Feature.objects.filter(uniquename=uniqueName)
                else:
                    feature = Feature.objects.filter(uniquename=uniqueName)
            geneLink = GeneLink(tag=tag, feature=feature)
            geneLink.save()
        except DatabaseError as e:
            transaction.rollback()
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))
        
        # limit metadata return
        metadata.limitFields(self.fields)
            
        metadata.put('id', geneLink.pk)
        metadata.put('tagId', geneLink.tag.pk)
        metadata.put('uniqueName', geneLink.feature.uniquename)
        metadata.put('name', geneLink.feature.name)
        metadata.put('organismId', geneLink.feature.organism.organism_id)
        
        return metadata
        
        