'''
    Pagelet for the user Workbench
    
    Author: Andrew Oberlin
    Date: July 23, 2012
'''
from renderEngine.PageletBase import PageletBase

class ImageManagerPagelet(PageletBase):
    '''
        Renders the user workbench for the website        
    
        Params: request -- the Django request object with the POST & GET args
        
        Returns: Dictionary of arguments for rendering this pagelet
    '''
    def doProcessRender(self, request):
        self.setLayout('registered/imageManager.html')

        return {}
