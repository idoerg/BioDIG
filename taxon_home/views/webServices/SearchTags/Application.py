'''
	Ajax Application for getting the metadata abourt an image
	URL: /images/getImageMetadata
	
	Author: Andrew Oberlin
	Date: July 23, 2012
'''
from renderEngine.AjaxApplicationBase import WebServiceApplicationBase
from renderEngine.WebServiceObject import WebServiceObject
import taxon_home.views.util.ErrorConstants as Errors
from django.views.decorators.csrf import csrf_exempt
import api.API as API

class Application(WebServiceApplicationBase):
	def doProcessRender(self, request):
		renderObj = WebServiceObject()		
		if (request.method == "GET"):
			renderObj = API.getImageTags(request)
		else:
			renderObj.setError(Errors.INVALID_METHOD.setMethod(request.method))

		self.setJsonObject(renderObj.getObject())
		self.setStatus(renderObj.getCode())
		
	
'''
	Used for mapping to the url in urls.py
'''
@csrf_exempt
def renderAction(request):
	return Application().render(request)
