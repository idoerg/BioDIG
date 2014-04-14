'''
	Pagelet for the Images Page

	Author: Andrew Oberlin
	Date: July 26, 2012
'''
from biodig.base.renderEngine.PageletBase import PageletBase
from biodig.base.models import Image

class ImagesPagelet(PageletBase):
	'''
		Renders the center of the home page

		Params: request -- the Django request object with the POST & GET args

		Returns: Dictionary of arguments for rendering this pagelet
	'''
	def doProcessRender(self, request):
		self.setLayout('public/images.html')

		if request.user and request.user.is_authenticated(): # apply user's permissions
			if request.user.is_staff:
				totalImages = Image.objects.all().count()
			else:
				images = Image.objects.filter(isPrivate=False) | Image.objects.filter(user=request.user)
				totalImages = images.count()
		else:
			totalImages = Image.objects.filter(isPrivate=False).count()

		return {
			'totalImages' : totalImages
		}
