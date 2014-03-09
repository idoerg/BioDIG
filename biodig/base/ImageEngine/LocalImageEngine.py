'''
Created on Mar 5, 2014

@author: Andrew Oberlin
'''

from biodig.base.ImageEngine import ImageEngine
import os
from django.conf import settings

class LocalImageEngine(ImageEngine):
    '''
        Saves the image and thumbnail in the media directory
        under thumbnails and pictures.
    '''
    images = os.path.join(settings.MEDIA_ROOT, 'pictures')
    thumbnails = os.path.join(settings.MEDIA_ROOT, 'thumbnails')
    
    def __init__(self):
        '''
            Creates the necessary directories for the images and
            thumbnails to be placed in.
        '''
        if not os.path.isdir(LocalImageEngine.images):
            os.mkdir(LocalImageEngine.images)
        
        if not os.path.isdir(LocalImageEngine.thumbnails):
            os.mkdir(LocalImageEngine.thumbnails)
    
    def saveImage(self, image):
        newloc = os.path.join(LocalImageEngine.images, os.path.basename(image))
        os.rename(image, newloc)
        return settings.MEDIA_URL + newloc
    
    def saveThumbnail(self, thumbnail):
        newloc = os.path.join(LocalImageEngine.images, os.path.basename(thumbnail))
        os.rename(thumbnail, newloc)
        return settings.MEDIA_URL + newloc
    
        