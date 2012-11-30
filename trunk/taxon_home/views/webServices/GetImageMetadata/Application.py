'''
	Ajax Application for getting the metadata abourt an image
	URL: /images/getImageMetadata
	
	Author: Andrew Oberlin
	Date: July 23, 2012
'''
from renderEngine.AjaxApplicationBase import WebServiceApplicationBase
from django.views.decorators.csrf import csrf_exempt
from mycoplasma_home.views.api import ImagesAPI

class Application(WebServiceApplicationBase):
	def doProcessRender(self, request):
		renderObj = {
			'error' : False,
			'errorMessage' : ImagesAPI.NO_ERROR
		}
		if request.REQUEST.has_key('imageKey'):
			# the key for lookup and the image it is attached to
			imageKey = request.REQUEST['imageKey']
			renderObj = ImagesAPI.getImageMetadata(imageKey, request.user)				
		else:
			renderObj['error'] = True
			renderObj['errorMessage'] = ImagesAPI.NO_IMAGE_KEY
		

		self.setJsonObject(renderObj)
		
	
'''
	Used for mapping to the url in urls.py
'''
@csrf_exempt
def renderAction(request):
	return Application().render(request)
