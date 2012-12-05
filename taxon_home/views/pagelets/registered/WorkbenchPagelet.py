'''
    Pagelet for the user Workbench
    
    Author: Andrew Oberlin
    Date: July 23, 2012
'''
from renderEngine.PageletBase import PageletBase
from multiuploader.models import Image
from taxon_home.models import Picture

class WorkbenchPagelet(PageletBase):
    '''
        Renders the user workbench for the website        
    
        Params: request -- the Django request object with the POST & GET args
        
        Returns: Dictionary of arguments for rendering this pagelet
    '''
    def doProcessRender(self, request):
        self.setLayout('registered/workbench.html')

        userImages = Picture.objects.filter(user__exact=request.user.pk)

        myImages = []
                
        #
        for image in userImages:
            permissions = 'public'
            if image.isPrivate:
                permissions = 'private'
            myImages.append({
                'permissions' : permissions,
                'image' : image
            })
        
        return {
            'myImages' : myImages
        }
