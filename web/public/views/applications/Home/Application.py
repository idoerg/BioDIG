'''
	Application for the Image Editor of the DOME
	URL: / or /index.html
	
	Author: Andrew Oberlin
	Date: August 5, 2012
'''
from base.renderEngine.ApplicationBase import ApplicationBase
from web.public.views.pagelets.NavBarPagelet import NavBarPagelet
from web.public.views.pagelets.HomePagelet import HomePagelet
from web.public.views.pagelets.FooterPagelet import FooterPagelet

class Application(ApplicationBase):
	def doProcessRender(self, request):
		args = {
			'title' : 'Homepage'
		}
		self.setApplicationLayout('public/base.html', args)
		self.addPageletBinding('navBar', NavBarPagelet(addHelpButton=True))
		self.addPageletBinding('center-1', HomePagelet())
		self.addPageletBinding('footer', FooterPagelet())
		
'''
	Used for mapping to the url in urls.py
'''        	
def renderAction(request):
	return Application().render(request)

