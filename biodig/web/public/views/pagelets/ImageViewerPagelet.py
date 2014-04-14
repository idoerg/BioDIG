'''
    Pagelet for the Image Editor which is both an admin
    and a public application

    Author: Andrew Oberlin
    Date: August 5, 2012
'''
from biodig.base.renderEngine.PageletBase import PageletBase
from django.core.exceptions import ObjectDoesNotExist

class ImageViewerPagelet(PageletBase):
    def __init__(self, image_id):
        self.image_id = image_id


    '''
        Renders the center of the home page

        Params: request -- the Django request object with the POST & GET args

        Returns: Dictionary of arguments for rendering this pagelet
    '''
    def doProcessRender(self, request):
        self.setLayout('public/imageviewer.html')
        try:
            image = Image.objects.get(pk__exact=self.image_id)
        except Image.DoesNotExist:
            self.setLayout('public/404Media.html')
            return {}

        return {
            image: image
        }
