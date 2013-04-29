'''
    Pagelet for the customization of the website

    Author: Andrew Oberlin
    Date: August 5, 2012
'''

from renderEngine.PageletBase import PageletBase
from django.core.exceptions import ObjectDoesNotExist

class CustomizePagelet(PageletBase):
    '''
        Renders the center of the home page        
    
        Params: request -- the Django request object with the POST & GET args
        
        Returns: Dictionary of arguments for rendering this pagelet
    '''
    def doProcessRender(self, request):
        self.setLayout('admin/customize.html')
        
        return {
            
        }
