'''
	Pagelet for the Nav Bar on many pages
	
	Author: Andrew Oberlin
	Date: July 23, 2012
'''
from renderEngine.PageletBase import PageletBase
from mycoplasma_home.models import NavBarOption, PictureType, PictureProp

class NavBarPagelet(PageletBase):
	def __init__(self, addHelpButton=False):
		self.addHelpButton = addHelpButton
	
	'''
		Renders the navigation bar for the website		
	
		Params: request -- the Django request object with the POST & GET args
		
		Returns: Dictionary of arguments for rendering this pagelet
	'''
	def doProcessRender(self, request):
		self.setLayout('public/navBar.html')
		
		is_admin_page = False
		
		if (request.method == "GET" and request.GET.has_key('add_login')):                
			is_admin_page = request.GET['add_login']
		
		optionsList = NavBarOption.objects.all().order_by('rank')
		bannertype_obj = PictureType.objects.get(imageType__exact="banner")
		banner_img = PictureProp.objects.get(type_id__exact=bannertype_obj.pk).picture_id
		banner_url = banner_img.imageName

		return {
			'optionsList' : optionsList,
			'banner_url' : banner_url,
			'is_admin_page' : is_admin_page,
			'addHelpButton' : self.addHelpButton
		}
