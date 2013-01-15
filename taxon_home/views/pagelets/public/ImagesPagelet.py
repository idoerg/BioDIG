'''
	Pagelet for the Images Page
	
	Author: Andrew Oberlin
	Date: July 26, 2012
'''
from renderEngine.PageletBase import PageletBase
from taxon_home.models import Picture

class ImagesPagelet(PageletBase):
	'''
		Renders the center of the home page		
	
		Params: request -- the Django request object with the POST & GET args
		
		Returns: Dictionary of arguments for rendering this pagelet
	'''
	def doProcessRender(self, request):
		self.setLayout('public/images.html')
	
		limit = 15
		numPics = Picture.objects.all().count()
		pages = numPics/limit + 1
		# sets the number of pictures to display in a row of the picture table generated

		return {
			'limit': limit,
			'pages' : pages,
			'totalImages' : numPics,
			'imagesPerRow' : 5
		}
