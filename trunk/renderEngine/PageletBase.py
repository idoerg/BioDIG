'''
    Pagelet Object for Django
	
	Author: Andrew Oberlin
	Date: July 22, 2012
'''
from django.conf import settings

class PageletBase:
	'''
		Do not override this method to set the pagelet layout
	'''
	def __init__(self):
		self.pageletLayout = 'index.html'
	
	'''
		Override this method to interact with the database
		or doany other processes that need to be done by this pagelet
		to properly render
		
		Params: request -- the Django request object with the POST & GET args
		
		Returns: Dictionary of arguments for rendering this pagelet
	'''
	def doProcessRender(self, request):
		return dict()
	
	'''
		Sets the pagelet layout
	'''
	def setLayout(self, layout):
		self.pageletLayout = layout
	

	'''
		Gets the pagelet layout	
	'''
	def getLayout(self):
		return self.pageletLayout
	
	'''
		Should not be overridden takes the arguments given by doProcessRender
		and adds other arguments that should be there
	'''
	def render(self, request):
		args = self.doProcessRender(request)
		args['MEDIA_URL'] = settings.MEDIA_URL
		args['SITE_URL'] = settings.SITE_URL
		return args
