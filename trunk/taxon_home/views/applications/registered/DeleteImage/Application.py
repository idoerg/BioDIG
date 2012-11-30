'''
	Ajax Application for the deleting an image
	URL: /administration/deleteImage
	
	Author: Andrew Oberlin
	Date: October 19, 2012
'''
from renderEngine.AjaxAdminApplicationBase import AjaxAdminApplicationBase
from django.views.decorators.csrf import csrf_exempt
from mycoplasma_home.models import Picture
from django.core.exceptions import ObjectDoesNotExist

NO_ERROR = 'Success'
INVALID_ACTION = 'Invalid action for service'
INVALID_IMAGE_KEY = 'Invalid Image Key Provided - No Image Deleted'
NO_IMAGE_KEY = 'No Image Key to Delete Image'

class Application(AjaxAdminApplicationBase):
	def doProcessRender(self, request):
		errorMessage = NO_ERROR
		if (request.method == "POST"):
			if (request.POST.has_key('imageKey')):
				imageKey = request.POST['imageKey']
				try:
					picture = Picture.objects.get(pk__exact=imageKey)
					picture.delete()
				except (ObjectDoesNotExist):
					errorMessage = INVALID_IMAGE_KEY
			else:
				errorMessage = NO_IMAGE_KEY
		else: 
			errorMessage = INVALID_ACTION
		
		self.setJsonObject({
			'error' : errorMessage != NO_ERROR,
			'errorMessage' : errorMessage
		})

		
'''
	Used for mapping to the url in urls.py
'''
@csrf_exempt			
def renderAction(request):
	return Application().render(request)
