'''
	Application for the Logout Handler of the DOME
	URL: /logout_handler
	
	Author: Andrew Oberlin
	Date: August 14, 2012
'''
from renderEngine.RegisteredApplicationBase import RegisteredApplicationBase
from mycoplasma_home.views.pagelets.registered.ImageSliderPagelet import ImageSliderPagelet 

class Application(RegisteredApplicationBase):
	def doProcessRender(self, request):
		args = {}
		
		self.setApplicationLayout('public/simple.html', args)
		self.addPageletBinding('center-1', ImageSliderPagelet())

'''
	Used for mapping to the url in urls.py
'''      	
def renderAction(request):
	return Application().render(request)

