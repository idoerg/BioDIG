import taxon_home.views.util.ErrorConstants as Errors
from taxon_home.models import Picture, PictureDefinitionTag, Organism
from django.core.exceptions import ObjectDoesNotExist
from renderEngine.WebServiceObject import WebServiceObject
from django.db import transaction, DatabaseError

class PutAPI:
    def __init__(self, user=None, fields=None):
        self.user = user
        self.fields = fields

    '''
        Edits the image metadata by adding the organisms with the designated organism
        ids or by editing the description
        
        @param imageKey: The primary key for the image or the image
        @param isKey: Whether the first argument is a key object or not (default: true)
        
        @return: A dictionary containing organisms associated with the image and all 
        of the images attributes. The dictionary will also contain error information
        stored in the errorMessage and error fields
    '''
    @transaction.commit_on_success 
    def editImageMetadata(self, imageKey, description, organisms, isKey=True):
        organisms = []
        metadata = WebServiceObject()
        
        try:
            if (isKey):
                image = Picture.objects.get(pk__exact=imageKey) 
            else:
                image = imageKey
            
            authenticated = True
            if image.isPrivate:
                if self.user and self.user.is_authenticated():
                    authenticated = image.user == self.user
                else:
                    authenticated = False
                    
            if authenticated:
                defTags = PictureDefinitionTag.objects.filter(picture__exact=image)
                
                organismField = not self.fields or 'organisms' in self.fields
                
                if organisms:
                    newOrganisms = Organism.objects.filter(organism_id__in=organisms)
                    newDefTags = []
                    for newOrg in newOrganisms:
                        newDefTags.append(PictureDefinitionTag(picture=image, organism=newOrg))
                    try:
                        defTags.delete()
                        for newTag in newDefTags:
                            newTag.save()
                            if organismField:
                                organisms.append({
                                    'commonName' : newTag.organism.common_name,
                                    'abbreviation' : newTag.organism.abbreviation,
                                    'genus' : newTag.organism.genus,
                                    'species' : newTag.organism.species,
                                    'id' : newTag.organism.pk
                                })
                    except DatabaseError as e:
                        transaction.rollback()
                        raise Errors.INTEGRITY_ERROR.setCustom(str(e))
                if description:
                    image.description = description
                    try:
                        image.save()
                    except DatabaseError as e:
                        transaction.rollback()
                        raise Errors.INTEGRITY_ERROR.setCustom(str(e))                   
            else:
                raise Errors.AUTHENTICATION
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_IMAGE_KEY
       
        if (not metadata.isError()):
            metadata.limitFields(self.fields)
            
            if not organisms and organismField:
                for defTag in defTags:
                    organisms.append({
                        'commonName' : defTag.organism.common_name,
                        'abbreviation' : defTag.organism.abbreviation,
                        'genus' : defTag.organism.genus,
                        'species' : defTag.organism.species,
                        'id' : defTag.organism.pk
                    })
            # put in the information we care about
            metadata.put('organisms', organisms)
            metadata.put('description', image.description)
            metadata.put('uploadedBy', image.user.username)
            metadata.put('uploadDate', image.uploadDate.strftime("%Y-%m-%d %H:%M:%S"))
            metadata.put('url', image.imageName.url)
            metadata.put('id', image.pk)
        
        return metadata