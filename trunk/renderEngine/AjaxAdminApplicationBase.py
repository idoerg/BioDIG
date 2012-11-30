'''
	This application uses the renderEngine to render pure JSON instead
	of a page. To be used in junction with Ajax

	Author: Andrew Oberlin
	Date: July 29, 2012
'''
from renderEngine.AjaxApplicationBase import AjaxApplicationBase

class AjaxAdminApplicationBase(AjaxApplicationBase):
	def render(self, request):
		if request.user.is_authenticated() and request.user.is_staff:
			self.doProcessRender(request)
			return self.renderEngine.renderJson(request)
		else:
			self.setJsonObject({ 'error' : True })
			return self.renderEngine.renderJson(request)
		

'''
	Used for mapping to the url in urls.py
'''        	
def renderAction(request):
	return AjaxAdminApplicationBase().render(request)
