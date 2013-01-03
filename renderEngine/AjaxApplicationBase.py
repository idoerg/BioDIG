'''
	This application uses the renderEngine to render pure JSON instead
	of a page. To be used in junction with Ajax

	Author: Andrew Oberlin
	Date: July 29, 2012
'''
from renderEngine.RenderEngine import RenderEngine
from django.conf import settings

class AjaxApplicationBase:
	def __init__(self):
		self.renderEngine = RenderEngine()
	
	def setJsonObject(self, obj):
		obj['SITE_URL'] = settings.SITE_URL
		obj['STATIC_URL'] = settings.STATIC_URL
		self.renderEngine.setApplicationLayout(obj)
	
	def setStatus(self, status):
		self.renderEngine.setStatus(status)
	
	'''
		Should be overridden, sets the applicationLayout
		and all of the pagelet bindings
	'''
	def doProcessRender(self, request):
		self.setApplicationLayout('base.html')
		
	def render(self, request):
		self.doProcessRender(request)
		return self.renderEngine.renderJson(request)

class WebServiceApplicationBase(AjaxApplicationBase):
	def setJsonObject(self, obj):
		self.renderEngine.setApplicationLayout(obj)
		
	def getJsonObject(self):
		return self.renderEngine.getApplicationLayout()
'''
	Used for mapping to the url in urls.py
'''        	
def renderAction(request):
	return AjaxApplicationBase().render(request)
