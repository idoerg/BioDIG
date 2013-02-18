import taxon_home.views.util.ErrorConstants as Errors
from taxon_home.models import Picture, PictureDefinitionTag
from django.core.exceptions import ObjectDoesNotExist
from renderEngine.WebServiceObject import WebServiceObject
from django.db import transaction, DatabaseError

class DeleteAPI:
    def __init__(self, user=None, fields=None):
        self.user = user
        self.fields = fields

    '''
        Deletes the image with the given key
        
        @param imageKey: The primary key for the image or the image
        @param isKey: Whether the first argument is a key object or not (default: true)
        
        @return: A dictionary containing organisms associated with the image and all 
        of the images attributes. The dictionary will also contain error information
        stored in the errorMessage and error fields
    '''
    @transaction.commit_on_success
    def deleteImage(self, imageKey, isKey=True):
        organisms = []
        metadata = WebServiceObject()
        
        try:
            if (isKey):
                image = Picture.objects.get(pk__exact=imageKey) 
            else:
                image = imageKey
        except (ObjectDoesNotExist, ValueError):
            raise Errors.INVALID_IMAGE_KEY
            
                
        if not image.writePermissions(self.user):
            raise Errors.AUTHENTICATION
        
        if not self.fields or 'organisms' in self.fields:
            defTags = PictureDefinitionTag.objects.filter(picture__exact=image)
            
            for tag in defTags:
                try:
                    organisms.append({
                        'commonName' : tag.organism.common_name,
                        'abbreviation' : tag.organism.abbreviation,
                        'genus' : tag.organism.genus,
                        'species' : tag.organism.species,
                        'id' : tag.organism.pk
                    })
                except ObjectDoesNotExist:
                    None
        
        metadata.limitFields(self.fields)

        # put in the information we care about
        metadata.put('organisms', organisms)
        metadata.put('description', image.description)
        metadata.put('uploadedBy', image.user.username)
        metadata.put('uploadDate', image.uploadDate.strftime("%Y-%m-%d %H:%M:%S"))
        metadata.put('url', image.imageName.url)
        metadata.put('id', image.pk)
        
        try:
            image.delete()
        except DatabaseError as e:
            transaction.rollback()
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))
        
        return metadata