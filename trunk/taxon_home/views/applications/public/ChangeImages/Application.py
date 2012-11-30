'''
	Ajax Application for the Image Pagination
	URL: /image_change
	
	Author: Andrew Oberlin
	Date: July 23, 2012
'''
from renderEngine.AjaxApplicationBase import AjaxApplicationBase
from django.views.decorators.csrf import csrf_exempt
from mycoplasma_home.models import PictureProp, Organism, PictureDefinitionTag

class Application(AjaxApplicationBase):
	def doProcessRender(self, request):
		error = request.method != 'POST'
		if (not error):
			if (request.POST.has_key('rangeX')):        
				rangeX = int(request.POST['rangeX'])
			else:
				rangeX = 0
			if (request.POST.has_key('rangeY')): 
				rangeY = int(request.POST['rangeY'])
			else:
				rangeY = 14
			
			num_items_row = 5
			
			allPics = True
			if (request.POST.has_key('organism') and request.POST['organism'] != ''):
				allPics = False
				organism = request.POST['organism']
			
			if (allPics == True):
				picture_props = PictureProp.objects.filter(type_id__imageType__exact="database_photo")[rangeX:rangeY+1]
				picture_list = list()                
				for prop in picture_props:
					pictureModel = prop.picture_id
					picture = {
						'pk' : pictureModel.pk,
						'imageName' : pictureModel.imageName.url,
						'description' : pictureModel.description
					}
					picture_list.append(picture)	
			else:
				if (int(organism) != -1):
					candidate = Organism.objects.get(pk__exact=int(organism))                
					picture_def_tags = PictureDefinitionTag.objects.filter(organism_id__exact=candidate.pk)[rangeX:rangeY+1]
				else:
					picture_def_tags = list()
				
				picture_list = list()                
				
				for tag in picture_def_tags:
					pictureModel = tag.picture
					picture = {
						'pk' : pictureModel.pk,
						'imageName' : pictureModel.imageName.url,
						'description' : pictureModel.description
					}
					picture_list.append(picture)

		renderObj = {
			'error' : error,
			'picturesList' : picture_list,
			'numItemsPerRow' : num_items_row
		}

		self.setJsonObject(renderObj)
'''
	Used for mapping to the url in urls.py
'''
@csrf_exempt        	
def renderAction(request):
	return Application().render(request)
