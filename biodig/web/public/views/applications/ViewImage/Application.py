'''
	Application for the Image Editor of the DOME (Administration and Public View)
	URL: /images/editor

	Author: Andrew Oberlin
	Date: August 20, 2012
'''
from biodig.base.renderEngine.ApplicationBase import ApplicationBase
from biodig.web.public.views.pagelets.NavBarPagelet import NavBarPagelet
from biodig.web.public.views.pagelets.FooterPagelet import FooterPagelet
from biodig.web.public.views.pagelets.ImageViewerPagelet import ImageViewerPagelet

class Application(ApplicationBase):
	def doProcessRender(self, request, image_id):
		args = {}
		self.addPageletBinding('navBar', NavBarPagelet(addHelpButton=True))

		args['title'] = 'Image Viewer'
		self.addPageletBinding('center-1', ImageViewerPagelet(image_id))

		self.setApplicationLayout('public/base.html', args)

		self.addPageletBinding('footer', FooterPagelet())

	def render(self, request, image_id):
		self.tokenAuthentication(request)
		self.doProcessRender(request, image_id)
		return self.renderEngine.render(request)
'''
	Used for mapping to the url in urls.py
'''
def renderAction(request, image_id):
	return Application().render(request, image_id)
