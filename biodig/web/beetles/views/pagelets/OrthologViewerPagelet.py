'''
    Pagelet for the BeetleDIG Ortholog Viewer Page
    
    Author: Asma Riyaz
    Date: MAy 26, 2014
'''
from biodig.base.renderEngine.PageletBase import PageletBase

class OrthologViewerPagelet(PageletBase):
    def __init__(self, TC_id):
        self.TC_id = TC_id

    '''
        Renders the center of the ortholog viewer   
    
        Params: request -- the Django request object with the POST & GET args
        
        Returns: Dictionary of arguments for rendering this pagelet
    '''
    def doProcessRender(self, request):
        self.setLayout('beetles/orthologviewer.html')
        return {
            'TC_id' : self.TC_id
        }
