'''
	Pagelet for the GBrowse Visualization
	
	Author: Andrew Oberlin
	Date: August 14, 2012
'''
from web.renderEngine.PageletBase import PageletBase

class GBrowsePagelet(PageletBase):
	'''
		Renders the center of the home page		
	
		Params: request -- the Django request object with the POST & GET args
		
		Returns: Dictionary of arguments for rendering this pagelet
	'''
	def doProcessRender(self, request):
		self.setLayout('public/gbrowse.html')
		args = {}
		if (request.REQUEST.has_key('organismId')):
			args['organismId'] = request.REQUEST['organismId']
			if (request.REQUEST.has_key('name')):
				args['name'] = request.REQUEST['name']
			if (request.REQUEST.has_key('uniquename')):
				args['uniquename'] = request.REQUEST['uniquename']
		return args
