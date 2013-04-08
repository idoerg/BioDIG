import taxon_home.views.util.ErrorConstants as Errors
from taxon_home.models import Tag, GeneLink, Feature
from django.core.exceptions import ObjectDoesNotExist
from renderEngine.WebServiceObject import WebServiceObject, LimitDict
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
    def createGeneLink(self, tagKey, name=None,  uniqueName=None, organismId=None, isKey=True):
        metadata = WebServiceObject()
        
        try:
            if isKey:
                tag = Tag.objects.get(pk__exact=tagKey)
            else:
                tag = tagKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_TAG_GROUP_KEY
        
        if not tag.writePermissions(self.user):
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
            
            if not feature:
                error = "Could not find a feature with the parameters: "
                if name and organismId:
                    error += "name: " + name + ", organismId: " + organismId
                if uniqueName:
                    comma = ", " if name and organismId else ""
                    error += comma + "uniqueName: " + uniqueName
                
                raise Errors.NO_MATCHING_FEATURE.setCustom(error)
            elif len(feature) > 1:
                error = "Multiple matches for parameters: "
                if name and organismId:
                    error += "name: " + name + ", organismId: " + organismId
                if uniqueName:
                    comma = ", " if name and organismId else ""
                    error += comma + "uniqueName: " + uniqueName
                    
                error += "\n\n Responses: \n\n"
                
                for f in feature:
                    error += "uniquename: " + f.uniquename + ", name: " + f.name + ", organism: " + f.organism.common_name + "\n\n"
                
                raise Errors.NO_MATCHING_FEATURE.setCustom(error)
            geneLink = GeneLink(tag=tag, feature=feature[0])
            geneLink.save()
        except DatabaseError as e:
            transaction.rollback()
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))
        
        # limit metadata return
        metadata.limitFields(self.fields)
            
        metadata.put('id', geneLink.pk)
        metadata.put('user', geneLink.user.username)
        metadata.put('tagId', geneLink.tag.pk)
        metadata.put('feature', 
            LimitDict(self.fields, {
                'uniqueName' : geneLink.feature.uniquename,
                'name' : geneLink.feature.name,
                'organismId' : geneLink.feature.organism.organism_id
            })
        )
        
        return metadata
        
        
