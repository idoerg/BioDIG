'''
	Application for the Image Editor of the DOME
	URL: / or /index.html

	Author: Andrew Oberlin
	Date: August 5, 2012
'''
from biodig.base.renderEngine.ApplicationBase import ApplicationBase
from biodig.web.public.views.pagelets.NavBarPagelet import NavBarPagelet
from biodig.web.public.views.pagelets.ActivatePagelet import ActivatePagelet
from biodig.web.public.views.pagelets.FooterPagelet import FooterPagelet

class Application(ApplicationBase):
	def doProcessRender(self, request, user_id, activation_key):
		args = {
			'title' : 'Activation Page'
		}
		self.setApplicationLayout('public/base.html', args)
		self.addPageletBinding('navBar', NavBarPagelet(addHelpButton=False))
		self.addPageletBinding('center-1', ActivatePagelet(user_id, activation_key))
		self.addPageletBinding('footer', FooterPagelet())

	def render(self, request, user_id, activation_key):
		self.tokenAuthentication(request)
		self.doProcessRender(request, user_id, activation_key)
		return self.renderEngine.render(request)

'''
    Used for mapping to the url in urls.py
'''
def renderAction(request, user_id, activation_key):
	return Application().render(request, user_id, activation_key)
