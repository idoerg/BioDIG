'''
	Application for the Logout Handler of the DOME
	URL: /logout_handler
	
	Author: Andrew Oberlin
	Date: August 14, 2012
'''
from renderEngine.AdminApplicationBase import AdminApplicationBase
from taxon_home.views.pagelets.registered.NavBarPagelet import NavBarPagelet
from taxon_home.views.pagelets.admin.CustomizePagelet import CustomizePagelet
from taxon_home.views.pagelets.public.FooterPagelet import FooterPagelet

class Application(AdminApplicationBase):
	def doProcessRender(self, request):
		args = {
			'title' : 'Customize'
		}
		
		self.setApplicationLayout('registered/base.html', args)
		self.addPageletBinding('navBar', NavBarPagelet())
		self.addPageletBinding('center-1', CustomizePagelet())
		self.addPageletBinding('footer', FooterPagelet())

'''
	Used for mapping to the url in urls.py
'''      	
def renderAction(request):
	return Application().render(request)

