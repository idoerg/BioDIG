'''
    Used in junction with the rendering engine to render a page that should only
    be accessed by an administrator

    Author: Andrew Oberlin
    Date: August 5, 2012
'''
from ApplicationBase import ApplicationBase
from django.shortcuts import redirect
from django.conf import settings

class RegisteredApplicationBase(ApplicationBase):
    def render(self, request):
        if request.user.is_authenticated():
            self.doProcessRender(request)
            return self.renderEngine.render(request)
        else:
            return redirect(settings.SITE_URL + '?add_login=True')
