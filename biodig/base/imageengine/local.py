'''
Created on Mar 5, 2014

@author: Andrew Oberlin
'''

from biodig.base.imageengine.engine import ImageEngine
from biodig.base.imageengine.exceptions import MissingFile
import os
from django.conf import settings

class LocalImageEngine(ImageEngine):
    '''
        Saves the image and thumbnail in the media directory
        under thumbnails and pictures.
    '''
    IMAGES_ROOT = os.path.join(settings.MEDIA_ROOT, 'pictures')
    THUMBNAILS_ROOT = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
    
    IMAGES_URL = settings.MEDIA_URL + 'pictures/'
    THUMBNAILS_URL = settings.MEDIA_URL + 'thumbnails/'
    
    def __init__(self):
        '''
            Creates the necessary directories for the images and
            thumbnails to be placed in.
        '''
        if not os.path.isdir(LocalImageEngine.IMAGES_ROOT):
            os.mkdir(LocalImageEngine.IMAGES_ROOT)
        
        if not os.path.isdir(LocalImageEngine.THUMBNAILS_ROOT):
            os.mkdir(LocalImageEngine.THUMBNAILS_ROOT)
    
    def save_image(self, image):
        base = os.path.basename(image)
        newloc = os.path.join(LocalImageEngine.IMAGES_ROOT, base)
        os.rename(image, newloc)
        return LocalImageEngine.IMAGES_URL + base
    
    def save_thumbnail(self, thumbnail):
        base = os.path.basename(thumbnail)
        newloc = os.path.join(LocalImageEngine.THUMBNAILS_ROOT, base)
        os.rename(thumbnail, newloc)
        return LocalImageEngine.THUMBNAILS_URL + base
    
    def delete_image(self, image):
        # strip off the prefix of MEDIA_URL from the image URL
        image = image.replace(settings.MEDIA_URL, '', 1)
        # add the root prefix for the file's location
        image = os.path.join(settings.MEDIA_ROOT, image)
        try:    # remove the file
            os.remove(image)
        except OSError:
            raise MissingFile()

    def delete_thumbnail(self, thumbnail):
        # strip off the prefix of MEDIA_URL from the image URL
        thumbnail = thumbnail.replace(settings.MEDIA_URL, '', 1)
        # add the root prefix for the file's location
        thumbnail = os.path.join(settings.MEDIA_ROOT, thumbnail)
        try:    # remove the file
            os.remove(thumbnail)
        except OSError:
            raise MissingFile()
