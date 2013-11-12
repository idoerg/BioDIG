'''
    Used in junction with the rendering engine to render a page

    Author: Andrew Oberlin
    Date: July 22, 2012
'''
from RenderEngine import RenderEngine
from rest_framework.authentication import TokenAuthentication

class ApplicationBase:
    def __init__(self):
        self.renderEngine = RenderEngine()
    
    def setApplicationLayout(self, applicationLayout, applicationArgs):
        self.renderEngine.setApplicationLayout(applicationLayout, applicationArgs)

    def setStatus(self, status):
        self.renderEngine.setStatus(status)

    def addPageletBinding(self, pageletName, pageletObj):
        self.renderEngine.addPageletBinding(pageletName, pageletObj)

    '''
        Should be overridden, sets the applicationLayout
        and all of the pagelet bindings
    '''
    def doProcessRender(self, request):
        self.setApplicationLayout('base.html')
        
    def tokenAuthentication(self, request):
        # default to session authentication
        if not request.user or not request.user.is_authenticated():
            try:
                auth = TokenAuthentication()
                user, token = auth.authenticate(request)
                request.user = user
            except Exception, e:
                pass #  ignore the attempt at authentication

    def render(self, request):
        self.tokenAuthentication(request)
        self.doProcessRender(request)
        return self.renderEngine.render(request)

'''
    Used for mapping to the url in urls.py
'''         
def renderAction(request):
    return ApplicationBase().render(request)
