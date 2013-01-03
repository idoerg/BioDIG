import taxon_home.views.api.ErrorConstants as Errors
from taxon_home.models import Picture, PictureDefinitionTag, Organism
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from renderEngine.WebServiceObject import WebServiceObject

'''
    Gets the metadata associated with an image given the image key
    
    @param imageKey: The primary key for the image or the image
    @param user: a Django auth_user object necessary for images
    that are still private
    @param isKey: Whether the first argument is a key object or not (default: true)
    
    @return: A dictionary containing organisms associated with the image and all 
    of the images attributes. The dictionary will also contain error information
    stored in the errorMessage and error fields
'''
def getImageMetadata(imageKey, user=None, isKey=True):
    organisms = []
    metadata = WebServiceObject()
    
    try:
        if (isKey):
            image = Picture.objects.get(pk__exact=imageKey) 
        else:
            image = imageKey
        
        authenticated = True
        if (image.isPrivate):
            if (user and user.is_authenticated()):
                authenticated = image.user == user
            else:
                authenticated = False
                
        if (authenticated):
            defTags = PictureDefinitionTag.objects.filter(picture__exact=image)
            
            for tag in defTags:
                try:
                    organisms.append(model_to_dict(Organism.objects.get(pk__exact=tag.organism_id), fields=['organism_id', 'common_name']))
                except ObjectDoesNotExist:
                    None                    
        else:
            metadata.error(Errors.AUTHENTICATION.getMessage(), Errors.AUTHENTICATION.getCode())
    except ObjectDoesNotExist:
        metadata.error(Errors.INVALID_IMAGE_KEY.getMessage(), Errors.INVALID_IMAGE_KEY.getCode())  
   
    if (not metadata.isError()):
        # put in the information we care about
        metadata.put('organisms', organisms)
        metadata.put('description', image.description)
        metadata.put('uploadedBy', image.user.username)
        metadata.put('uploadDate', image.uploadDate.strftime("%Y-%m-%d %H:%M:%S"))
        metadata.put('url', image.imageName.url)
    
    return metadata