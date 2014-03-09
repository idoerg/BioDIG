'''
	Application for the Image Editor of the DOME (Administration and Public View)
	URL: /images/editor
	
	Author: Andrew Oberlin
	Date: August 20, 2012
'''
from biodig.base.renderEngine.ApplicationBase import ApplicationBase
from biodig.web.public.views.pagelets.NavBarPagelet import NavBarPagelet
from biodig.web.public.views.pagelets.FooterPagelet import FooterPagelet
from biodig.web.public.views.pagelets.ImageEditorPagelet import ImageEditorPagelet as PublicPagelet
from biodig.web.admin.views.pagelets.ImageEditorPagelet import ImageEditorPagelet as AdminPagelet

class Application(ApplicationBase):
	def doProcessRender(self, request):
		args = {}
		self.addPageletBinding('navBar', NavBarPagelet(addHelpButton=True))
		
		args['title'] = 'Image Viewer'
		self.addPageletBinding('center-1', PublicPagelet())
			
		self.setApplicationLayout('public/base.html', args)
			
		self.addPageletBinding('footer', FooterPagelet())
		

'''
	Used for mapping to the url in urls.py
'''        	
def renderAction(request):
	return Application().render(request)

