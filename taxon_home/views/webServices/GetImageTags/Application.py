'''
	Ajax Application for getting tags related to the image
	URL: /images/getTags
	
	Author: Andrew Oberlin
	Date: July 23, 2012
'''
from renderEngine.AjaxApplicationBase import WebServiceApplicationBase
from django.views.decorators.csrf import csrf_exempt
from mycoplasma_home.views.api import ImagesAPI

class Application(WebServiceApplicationBase):
	def doProcessRender(self, request):
		if request.REQUEST.has_key('tagGroupKey'):
			# the key for lookup and the image it is attached to
			tagGroupKey = request.REQUEST['tagGroupKey']
			tags = ImagesAPI.getImageTags(tagGroupKey, user=request.user, isKey=True)
			self.setJsonObject(tags)
		else:
			self.setJsonObject({
				'error' : True,
				'errorMessage' : ImagesAPI.NO_TAG_GROUP_KEY
			})
'''
	Used for mapping to the url in urls.py
'''
@csrf_exempt
def renderAction(request):
	return Application().render(request)
