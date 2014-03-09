import taxon_home.views.util.ErrorConstants as Errors
from taxon_home.models import Picture, PictureDefinitionTag, Organism
from renderEngine.WebServiceObject import WebServiceObject
from django.db import transaction, DatabaseError
from PIL import Image as PILImage
import imghdr
import os
import cStringIO
import hashlib
from django.core.files.uploadedfile import UploadedFile
from django.core.files import File
from django.conf import settings
import time

def handleUpload(upload):
    # gets the original file name and sets up the new location in the tmp
    now = str(time.time())
    originalFileName = os.path.join(
        os.path.join(
            settings.MEDIA_ROOT, os.path.join('cache', 'pictures')
        ), 
        now + upload.name
    )
    
    # writes the chunks in the file upload to the cache file
    destination = open(originalFileName, 'wb+')
    for chunk in upload.chunks():
        destination.write(chunk)
    destination.close()
    
    
    imageFile = PILImage.open(open(originalFileName, 'rb'))  

    # saves the file as a PNG
    thumbfile = cStringIO.StringIO()
    imageFile.save(thumbfile, 'PNG')
    
    imageHash = hashlib.md5(thumbfile.getvalue()).hexdigest()
    
    # changes the name of the image in the tmp to its new name
    filename = os.path.join(
        os.path.join(
            settings.MEDIA_ROOT, os.path.join('cache', 'pictures')
        ), 
        now + imageHash + '.png'
    )

    imageFile.save(open(filename, 'wb+'), 'PNG')
    os.remove(originalFileName)
    
    # gets the name of the thumbnail when it is changed
    thumbnailName = os.path.join(
        os.path.join(
            settings.MEDIA_ROOT, os.path.join('cache', 'thumbnails')
        ), 
        now + imageHash + '.png'
    )
    
    # changes the size of the thumbnail and saves it
    size = (125, 125)
    imageFile.thumbnail(size, PILImage.ANTIALIAS)
    imageFile.save(open(thumbnailName, 'wb+'), 'PNG')

    return (UploadedFile(File(open(filename, 'rb'))), UploadedFile(File(open(thumbnailName, 'rb'))), filename, thumbnailName)

class PostAPI:
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
    def createImageMetadata(self, image, description, altText, organisms, isKey=True):
        organismsArr = []
        metadata = WebServiceObject()
        
        if not (self.user and self.user.is_authenticated()):
            raise Errors.AUTHENTICATION
        filetype = imghdr.what(image.file)
        if not filetype or filetype not in set(['gif', 'tiff', 'jpeg', 'bmp', 'png']):
            raise Errors.INVALID_IMAGE_TYPE
        wrappedFile, thumbnailFile, filename, thumbnailName = handleUpload(image)
        
        
        if self.user.is_staff:
            upload = Picture(user=self.user, isPrivate=False, imageName=wrappedFile.file, thumbnail=thumbnailFile.file)
        else:
            upload = Picture(user=self.user, isPrivate=True, imageName=wrappedFile.file, thumbnail=thumbnailFile.file)            
        
        try:
            upload.save()
        except DatabaseError as e:
            transaction.rollback()
            os.remove(filename)
            os.remove(thumbnailName)
            raise Errors.INTEGRITY_ERROR.setCustom(str(e))
        
        os.remove(filename)
        os.remove(thumbnailName)
        
        # now that image has been properly uploaded add the metadata to it
        
        organismField = not self.fields or 'organisms' in self.fields
        
        if organisms:
            newOrganisms = Organism.objects.filter(organism_id__in=organisms)
            newDefTags = []
            for newOrg in newOrganisms:
                newDefTags.append(PictureDefinitionTag(picture=upload, organism=newOrg))
            try:
                for newTag in newDefTags:
                    newTag.save()
                    if organismField:
                        organismsArr.append({
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
            upload.description = description
            try:
                upload.save()
            except DatabaseError as e:
                transaction.rollback()
                raise Errors.INTEGRITY_ERROR.setCustom(str(e))
            
        if altText:
            upload.altText = altText
            try:
                upload.save()
            except DatabaseError as e:
                transaction.rollback()
                raise Errors.INTEGRITY_ERROR.setCustom(str(e))
        
        metadata.limitFields(self.fields)
        # put in the information we care about
        metadata.put('organisms', organismsArr)
        metadata.put('description', upload.description)
        metadata.put('altText', upload.altText)
        metadata.put('uploadedBy', upload.user.username)
        metadata.put('uploadDate', upload.uploadDate.strftime("%Y-%m-%d %H:%M:%S"))
        metadata.put('url', upload.imageName.url)
        metadata.put('thumbnail', upload.thumbnail.url)
        metadata.put('id', upload.pk)
            
        return metadata