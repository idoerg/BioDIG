'''
    Application for the Image Editor of the DOME
    URL: / or /index.html
    
    Author: Andrew Oberlin
    Date: August 5, 2012
'''
from biodig.base.renderEngine.ApplicationBase import ApplicationBase
from biodig.web.beetles.views.pagelets.OrthologViewerPagelet import OrthologViewerPagelet

class Application(ApplicationBase):
    def doProcessRender(self, request, TC_id):
        args = {
            'title' : 'Orthologs'
        }
        self.setApplicationLayout('beetles/base.html', args)
        self.addPageletBinding('main', OrthologViewerPagelet(TC_id))
        
        
    def render(self, request, TC_id):
        self.tokenAuthentication(request)
        self.doProcessRender(request, TC_id)
        return self.renderEngine.render(request)

'''
    Used for mapping to the url in urls.py
'''            
def renderAction(request, TC_id):
    return Application().render(request, TC_id)

