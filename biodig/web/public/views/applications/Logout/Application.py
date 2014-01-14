'''
	Application for the Logout Handler of the DOME
	URL: /logout_handler
	
	Author: Andrew Oberlin
	Date: August 14, 2012
'''
from biodig.base.renderEngine.ApplicationBase import ApplicationBase
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout

class Application(ApplicationBase):
	def doProcessRender(self, request):
		logout(request)

	def render(self, request):
		self.doProcessRender(request)
		return HttpResponseRedirect(
			reverse('web.public.views.applications.Home.Application.renderAction')
		)


'''
	Used for mapping to the url in urls.py
'''  
@csrf_exempt      	
def renderAction(request):
	return Application().render(request)

