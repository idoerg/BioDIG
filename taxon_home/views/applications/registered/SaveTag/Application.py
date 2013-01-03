'''
	Ajax Application for the Image Pagination
	URL: /administration/addNewTag
	
	Author: Andrew Oberlin
	Date: July 23, 2012
'''
from renderEngine.AjaxRegisteredApplicationBase import AjaxRegisteredApplicationBase
from taxon_home.views.util.Util import getMultiListPost
from django.views.decorators.csrf import csrf_exempt
from taxon_home.models import TagColor, Tag, TagGroup, TagPoint
from django.core.exceptions import ObjectDoesNotExist

class Application(AjaxRegisteredApplicationBase):
	def doProcessRender(self, request):
		errorMessage = None
		errorTagGroups = []
		tagKeys = {}
		if (request.method == "POST"):
			try:
				tagGroupKeys = request.POST.getlist('tagGroupKeys[]')
				description = request.POST['description']
				points = getMultiListPost(request, 'points')
				color = request.POST.getlist('color[]')
				
				if (len(color) >= 3):
					# first check if the color exists
					(tagColor, created) = TagColor.objects.get_or_create(red=color[0], green=color[1], blue=color[2])
					for key in tagGroupKeys:
						try:
							tagGroup = TagGroup.objects.get(pk__exact=key)
							if (tagGroup.picture.isPrivate and request.user == tagGroup.user) or not tagGroup.picture.isPrivate:
								newTag = Tag(description=description, color=tagColor, group=tagGroup, user=request.user)
								newTag.save()
								tagKeys[key] = newTag.pk
								
								for key, point in points.items():
									newTagPoint = TagPoint(tag=newTag, pointX=float(point[0]), pointY=float(point[1]), rank=int(key)+1)
									newTagPoint.save()
							else:
								errorMessage = "Incorrect permissions for editing this image or tag group"
						except ObjectDoesNotExist:
							errorTagGroups.append(key)
					
				else:
					errorMessage = "Incorrect format for color"	
			except KeyError as e:
				errorMessage = "Missing arguments in save for key: " + str(e)
		else:
			errorMessage = "Incorrect method for saving a tag"

		if (errorMessage == None and len(errorTagGroups) == 0):
			self.setJsonObject({
				'error' : False,
				'tagKeys' : tagKeys,
				'errorMessage' : errorMessage
			})
		elif len(errorTagGroups) > 0:
			self.setJsonObject({
				'error' : True,
				'errorMessage' : errorMessage + ' and these tag groups do not exist',
				'errorTagGroups' : errorTagGroups 
			})
		else:
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
