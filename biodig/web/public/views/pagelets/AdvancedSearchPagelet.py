'''
	Pagelet for the Advanced Search Page
	
	Author: Andrew Oberlin
	Date: January 31, 2013
'''
from biodig.base.renderEngine.PageletBase import PageletBase

class AdvancedSearchPagelet(PageletBase):
	'''
		Renders the center of the home page		
	
		Params: request -- the Django request object with the POST & GET args
		
		Returns: Dictionary of arguments for rendering this pagelet
	'''
	def doProcessRender(self, request):
		self.setLayout('public/advancedSearch.html')

		return {}
