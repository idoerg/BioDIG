'''
    Ajax Application for getting the metadata abourt an image
    URL: /images/getImageMetadata
    
    Author: Andrew Oberlin
    Date: July 23, 2012
'''
from biodig.base.renderEngine.AjaxApplicationBase import WebServiceApplicationBase
from biodig.base.renderEngine.WebServiceObject import WebServiceObject
from django.views.decorators.csrf import csrf_exempt
import api.API as API
import biodig.base.util.ErrorConstants as Errors

class Application(WebServiceApplicationBase):
    def doProcessRender(self, request):
        renderObj = WebServiceObject()
        try:
            if (request.method == "GET"):
                renderObj = API.getOrganisms(request)
            else:
                renderObj.setError(Errors.INVALID_METHOD.setCustom(request.method))
        except Errors.WebServiceException as e:
            renderObj.setError(e)

        self.setJsonObject(renderObj.getObject())
        self.setStatus(renderObj.getCode())
        
    
'''
    Used for mapping to the url in urls.py
'''
@csrf_exempt
def renderAction(request):
    return Application().render(request)
