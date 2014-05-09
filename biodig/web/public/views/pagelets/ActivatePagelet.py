'''
    Pagelet for the Activation Page

    Author: Andrew Oberlin
    Date: May 9, 2014
'''
from biodig.base.renderEngine.PageletBase import PageletBase
from django.contrib.auth.models import User

class ActivatePagelet(PageletBase):
    def __init__(self, user_id, activation_key):
        self.user_id = user_id
        self.activation_key = activation_key

    '''
        Renders the center of the home page

        Params: request -- the Django request object with the POST & GET args

        Returns: Dictionary of arguments for rendering this pagelet
    '''
    def doProcessRender(self, request):
        self.setLayout('public/activate.html')

        return {
            'user_id' : self.user_id,
            'activation_key' : self.activation_key
        }
