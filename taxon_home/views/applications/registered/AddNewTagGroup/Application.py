'''
	Ajax Application for the Image Pagination
	URL: /image/editor/submit
	
	Author: Andrew Oberlin
	Date: July 23, 2012
'''
from renderEngine.AjaxRegisteredApplicationBase import AjaxRegisteredApplicationBase
from django.views.decorators.csrf import csrf_exempt
from taxon_home.models import TagGroup, Picture
from django.core.exceptions import ObjectDoesNotExist

class Application(AjaxRegisteredApplicationBase):
	def doProcessRender(self, request):
		errorMessage = ""
		if (request.method == "POST" and request.POST.has_key('name')):
			if (request.POST.has_key('imageKey')):
				name = request.POST['name']
				imageKey = request.POST['imageKey']
				image = None
				try:
					image = Picture.objects.get(pk__exact=imageKey)
				except ObjectDoesNotExist:
					errorMessage = "Image does not exist"
				
				if (image != None):
					newTagGroup = TagGroup(user=request.user, name=name, picture=image)
					try:
						newTagGroup.save()
						self.setJsonObject({
							'error' : False,
							'tagGroup' : {
								'pk' : newTagGroup.pk,
								'tags' : [],
								'name' : newTagGroup.name,
								'dateCreated' : newTagGroup.dateCreated.strftime("%Y-%m-%d %H:%M:%S"),
								'lastModified' : newTagGroup.lastModified.strftime("%Y-%m-%d %H:%M:%S")
							}
						})
					except Exception:
						errorMessage = "Name provided has been used"
			else:
				errorMessage = "No image key provided for the new tag group"
		else:
			errorMessage = "No name provided for a new group"
		
		if (errorMessage != ""):
			self.setJsonObject({
				'error' : True,
				'errorMessage' : errorMessage
			})

		
'''
	Used for mapping to the url in urls.py
'''
@csrf_exempt			
def renderAction(request):
	return Application().render(request)
