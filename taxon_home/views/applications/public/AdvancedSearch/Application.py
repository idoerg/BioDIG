'''
	Application for the Search Page of the DOME
	URL: / or /index.html
	
	Author: Andrew Oberlin
	Date: August 5, 2012
'''
from renderEngine.ApplicationBase import ApplicationBase
from taxon_home.views.pagelets.public.NavBarPagelet import NavBarPagelet
from taxon_home.views.pagelets.public.FooterPagelet import FooterPagelet
from taxon_home.views.pagelets.public.AdvancedSearchPagelet import AdvancedSearchPagelet

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

