'''
	Application for the Login Handler of the DOME
	URL: /login_handler
	
	Author: Andrew Oberlin
	Date: August 14, 2012
'''
from renderEngine.ApplicationBase import ApplicationBase
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login 

class Application(ApplicationBase):
	def doProcessRender(self, request):
		if (request.method == "POST"):
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None and user.is_active:
				login(request, user)

	def render(self, request):
		self.doProcessRender(request)
		return HttpResponseRedirect(
			reverse('mycoplasma_home.views.applications.public.Home.Application.renderAction')
		)


'''
	Used for mapping to the url in urls.py
'''  
@csrf_exempt      	
def renderAction(request):
	return Application().render(request)

