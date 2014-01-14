'''
    This application uses the renderEngine to render pure JSON instead
    of a page. To be used in junction with Ajax

    Author: Andrew Oberlin
    Date: July 29, 2012
'''
from renderEngine.AjaxApplicationBase import AjaxApplicationBase

class AjaxRegisteredApplicationBase(AjaxApplicationBase):
    def render(self, request):
        self.tokenAuthentication(request)
        
        if request.user.is_authenticated():
            self.doProcessRender(request)
            return self.renderEngine.renderJson(request)
        else:
            self.setJsonObject({ 'error' : True })
            return self.renderEngine.renderJson(request)
        

'''
    Used for mapping to the url in urls.py
'''         
def renderAction(request):
    return AjaxRegisteredApplicationBase().render(request)
