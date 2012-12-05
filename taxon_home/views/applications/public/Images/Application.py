'''
	Application for the Images Page of the DOME
	URL: /images
	
	Author: Andrew Oberlin
	Date: July 23, 2012
'''
from renderEngine.ApplicationBase import ApplicationBase
from taxon_home.views.pagelets.public.NavBarPagelet import NavBarPagelet
from taxon_home.views.pagelets.public.ImagesPagelet import ImagesPagelet
from taxon_home.views.pagelets.public.FooterPagelet import FooterPagelet

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
