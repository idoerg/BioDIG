'''
	Pagelet for the Nav Bar on many pages
	
	Author: Andrew Oberlin
	Date: July 23, 2012
'''
from biodig.base.renderEngine.PageletBase import PageletBase

class NavBarPagelet(PageletBase):
	'''
		Renders the navigation bar for the website		
	
		Params: request -- the Django request object with the POST & GET args
		
		Returns: Dictionary of arguments for rendering this pagelet
	'''
	def doProcessRender(self, request):
		self.setLayout('registered/navBar.html')
		return {}
