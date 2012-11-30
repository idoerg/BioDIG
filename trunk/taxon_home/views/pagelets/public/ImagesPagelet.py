'''
	Pagelet for the Images Page
	
	Author: Andrew Oberlin
	Date: July 26, 2012
'''
from renderEngine.PageletBase import PageletBase
from mycoplasma_home.models import PictureProp

class ImagesPagelet(PageletBase):
	'''
		Renders the center of the home page		
	
		Params: request -- the Django request object with the POST & GET args
		
		Returns: Dictionary of arguments for rendering this pagelet
	'''
	def doProcessRender(self, request):
		self.setLayout('public/images.html')
	
		num_items_row = 5
		num_items_col = 3
		picsPerPage = num_items_row * num_items_col	  
		numPics = PictureProp.objects.filter(type_id__imageType__exact = "database_photo").count()
		numPicPages = numPics/picsPerPage + 1
		# sets the number of pictures to display in a row of the picture table generated

		return {
			'picsPerPage': picsPerPage,
			'numPages': numPicPages,
			'numImages': numPics
		}
