'''
    Application for the Image Editor of the DOME
    URL: / or /index.html
    
    Author: Andrew Oberlin
    Date: August 5, 2012
'''
from biodig.base.renderEngine.ApplicationBase import ApplicationBase
from biodig.web.public.views.pagelets.NavBarPagelet import NavBarPagelet
from biodig.web.public.views.pagelets.BlastPagelet import BlastPagelet

class Application(ApplicationBase):
    def doProcessRender(self, request):
        args = {
            'title' : 'Blast'
        }
        self.setApplicationLayout('public/base.html', args)
        self.addPageletBinding('navBar', NavBarPagelet())
        self.addPageletBinding('center-1', BlastPagelet())

'''
    Used for mapping to the url in urls.py
'''            
def renderAction(request):
    return Application().render(request)

