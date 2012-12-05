'''
	Application for the Logout Handler of the DOME
	URL: /logout_handler
	
	Author: Andrew Oberlin
	Date: August 14, 2012
'''
from renderEngine.RegisteredApplicationBase import RegisteredApplicationBase
from mycoplasma_home.views.pagelets.registered.NavBarPagelet import NavBarPagelet
from mycoplasma_home.views.pagelets.registered.ImageManagerPagelet import ImageManagerPagelet 

class Application(RegisteredApplicationBase):
	def doProcessRender(self, request):
		args = {
			'title' : 'Image Manager'
		}
		
		self.setApplicationLayout('registered/base.html', args)
		self.addPageletBinding('navBar', NavBarPagelet())
		self.addPageletBinding('center-1', ImageManagerPagelet())

'''
	Used for mapping to the url in urls.py
'''      	
def renderAction(request):
	return Application().render(request)

