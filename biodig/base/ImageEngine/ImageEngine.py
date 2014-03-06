'''
Created on Mar 5, 2014

@author: Andrew Oberlin
'''
from abc import ABCMeta, abstractmethod

class ImageEngine(object):
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def thumbnail(self, image):
        '''
            Creates a thumbnail from the image and returns the 
            
            @return: A smaller less clear version of the image for
            
        '''
        pass
    
    @abstractmethod
    def save(self, image, thumbnail):
        '''
            Saves the given image and thumbnail to the storage
            place and returns the url.
            
            @param image: 
        '''
        pass
    