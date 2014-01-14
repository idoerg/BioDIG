'''
	Application for the Search Page of the DOME
	URL: / or /index.html
	
	Author: Andrew Oberlin
	Date: August 5, 2012
'''
from biodig.base.renderEngine.ApplicationBase import ApplicationBase
from biodig.web.public.views.pagelets.NavBarPagelet import NavBarPagelet
from biodig.web.public.views.pagelets.FooterPagelet import FooterPagelet
from biodig.web.public.views.pagelets.AdvancedSearchPagelet import AdvancedSearchPagelet

class Application(ApplicationBase):
	def doProcessRender(self, request):
		args = {
			'title' : 'Advanced Search'
		}
		
		self.setApplicationLayout('public/base.html', args)
		
		self.addPageletBinding('navBar', NavBarPagelet())
		self.addPageletBinding('center-1', AdvancedSearchPagelet())
		self.addPageletBinding('footer', FooterPagelet())

'''
	Used for mapping to the url in urls.py
'''			
def renderAction(request):
	return Application().render(request)

