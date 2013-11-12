'''
    This application uses the renderEngine to render pure JSON instead
    of a page. To be used in junction with Ajax

    Author: Andrew Oberlin
    Date: July 29, 2012
'''
from RenderEngine import RenderEngine
from django.conf import settings
import time
from django.core.cache import cache
from WebServiceException import THROTTLED, WebServiceException
from WebServiceObject import WebServiceObject
from ApplicationBase import ApplicationBase

class AjaxApplicationBase(ApplicationBase):
    '''
    
    '''
    def __init__(self, extra=''):
        self.renderEngine = RenderEngine()
        self.extra = extra
    
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
        self.tokenAuthentication(request)

        try:
            if hasattr(settings, 'RATE_LIMIT'):
                self.throttle(request)
            self.coerce_put_post(request)
            self.coerce_delete_post(request)
            self.doProcessRender(request)
        except WebServiceException as e:
            renderObj = WebServiceObject()
            renderObj.setError(e)
            self.setJsonObject(renderObj.getObject())
            self.setStatus(renderObj.getCode())
        return self.renderEngine.renderJson(request)
    
    '''
        Coerces the request object to have a put query dict
        in order to separate it for the REST API
        
        Thanks to: Django Piston for this snippet
    '''   
    def coerce_delete_post(self, request):
        if request.method == "DELETE":
            # Bug fix: if _load_post_and_files has already been called, for
            # example by middleware accessing request.POST, the below code to
            # pretend the request is a POST instead of a PUT will be too late
            # to make a difference. Also calling _load_post_and_files will result 
            # in the following exception:
            #   AttributeError: You cannot set the upload handlers after the upload has been processed.
            # The fix is to check for the presence of the _post field which is set 
            # the first time _load_post_and_files is called (both by wsgi.py and 
            # modpython.py). If it's set, the request has to be 'reset' to redo
            # the query value parsing in POST mode.
            if hasattr(request, '_post'):
                del request._post
                del request._files
            
            try:
                request.method = "POST"
                request._load_post_and_files()
                request.method = "DELETE"
            except AttributeError:
                request.META['REQUEST_METHOD'] = 'POST'
                request._load_post_and_files()
                request.META['REQUEST_METHOD'] = 'DELETE'
                
            request.DELETE = request.POST
    
    '''
        Coerces the request object to have a put query dict
        in order to separate it for the REST API
        
        Thanks to: Django Piston for this snippet
    '''   
    def coerce_put_post(self, request):
        if request.method == "PUT":
            # Bug fix: if _load_post_and_files has already been called, for
            # example by middleware accessing request.POST, the below code to
            # pretend the request is a POST instead of a PUT will be too late
            # to make a difference. Also calling _load_post_and_files will result 
            # in the following exception:
            #   AttributeError: You cannot set the upload handlers after the upload has been processed.
            # The fix is to check for the presence of the _post field which is set 
            # the first time _load_post_and_files is called (both by wsgi.py and 
            # modpython.py). If it's set, the request has to be 'reset' to redo
            # the query value parsing in POST mode.
            if hasattr(request, '_post'):
                del request._post
                del request._files
            
            try:
                request.method = "POST"
                request._load_post_and_files()
                request.method = "PUT"
            except AttributeError:
                request.META['REQUEST_METHOD'] = 'POST'
                request._load_post_and_files()
                request.META['REQUEST_METHOD'] = 'PUT'
                
            request.PUT = request.POST
        
    '''
        Throttles a web service or ajax application to limit
        the use of the web service 
        
        Thanks to: Django Piston for this snippet
    '''    
    def throttle(self, request):
        if request.user.is_authenticated():
            ident = request.user.username
        else:
            ident = request.META.get('REMOTE_ADDR', None)
    
        if hasattr(request, 'throttle_extra'):
            """
                Since we want to be able to throttle on a per-
                application basis, it's important that we realize
                that `throttle_extra` might be set on the request
                object. If so, append the identifier name with it.
            """
            ident += ':%s' % str(request.throttle_extra)
        
        if ident:
            """
                Preferrably we'd use incr/decr here, since they're
                atomic in memcached, but it's in django-trunk so we
                can't use it yet. If someone sees this after it's in
                stable, you can change it here.
            """
            ident += ':%s' % self.extra
    
            now = time.time()
            count, expiration = cache.get(ident, (1, None))

            if expiration is None:
                expiration = now + settings.TIMEOUT * 60

            if count > settings.MAX_REQUESTS and expiration > now:
                e = THROTTLED
                e.setCustom(int((expiration - now)/60))
                raise e

            cache.set(ident, (count+1, expiration), (expiration - now))


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
