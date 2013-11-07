'''
	Application for the GBrowse Visualizer of the DOME
	URL: /browse
	
	Author: Andrew Oberlin
	Date: August 5, 2012
'''
from base.renderEngine.ApplicationBase import ApplicationBase
from web.public.views.pagelets.NavBarPagelet import NavBarPagelet
from web.public.views.pagelets.GBrowsePagelet import GBrowsePagelet
from web.public.views.pagelets.FooterPagelet import FooterPagelet

class Application(ApplicationBase):
	def doProcessRender(self, request):
		args = {
			'title' : 'GBrowse'
		}
		self.setApplicationLayout('public/base.html', args)
		self.addPageletBinding('navBar', NavBarPagelet())
		self.addPageletBinding('center-1', GBrowsePagelet())
		self.addPageletBinding('footer', FooterPagelet())

'''
	Used for mapping to the url in urls.py
'''        	
def renderAction(request):
	return Application().render(request)

