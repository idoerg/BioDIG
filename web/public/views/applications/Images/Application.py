'''
	Application for the Images Page of the DOME
	URL: /images
	
	Author: Andrew Oberlin
	Date: July 23, 2012
'''
from base.renderEngine.ApplicationBase import ApplicationBase
from web.public.views.pagelets.NavBarPagelet import NavBarPagelet
from web.public.views.pagelets.ImagesPagelet import ImagesPagelet
from web.public.views.pagelets.FooterPagelet import FooterPagelet

class Application(ApplicationBase):
	def doProcessRender(self, request):
		args = {
			'title' : 'Images'
		}
		self.setApplicationLayout('public/base.html', args)
		self.addPageletBinding('navBar', NavBarPagelet())
		self.addPageletBinding('center-1', ImagesPagelet())
		self.addPageletBinding('footer', FooterPagelet())
		
'''
	Used for mapping to the url in urls.py
'''
def renderAction(request):
	return Application().render(request)
