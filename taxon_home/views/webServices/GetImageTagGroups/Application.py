'''
	Ajax Application for getting tags related to the image
	URL: /images/getTagGroups
	
	Author: Andrew Oberlin
	Date: July 23, 2012
'''
from renderEngine.AjaxApplicationBase import WebServiceApplicationBase
from django.views.decorators.csrf import csrf_exempt
from mycoplasma_home.views.api import ImagesAPI

NO_ERROR = 'Success'
INVALID_IMAGE_KEY = 'Invalid Image Key Provided'
NO_IMAGE_KEY = 'No Image Key Provided'

class Application(WebServiceApplicationBase):
	def doProcessRender(self, request):
		renderObj = {
			'error' : False,
			'errorMessage' : ImagesAPI.NO_ERROR,
		}
		
		if request.REQUEST.has_key('imageKey'):
			# the key for lookup and the image it is attached to
			imageKey = request.REQUEST['imageKey']
			getTags = False
			if(request.REQUEST.has_key('getTags')):
				getTags = request.REQUEST['getTags'].lower() == 'true'
			
			renderObj = ImagesAPI.getImageTagGroups(imageKey, user=request.user, getTags=getTags, isKey=True)			
		else:
			renderObj['error'] = True
			renderObj['errorMessage'] = NO_IMAGE_KEY


		self.setJsonObject(renderObj)
'''
	Used for mapping to the url in urls.py
'''
@csrf_exempt
def renderAction(request):
	return Application().render(request)
