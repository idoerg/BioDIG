from renderEngine.WebServiceObject import WebServiceObject
import taxon_home.views.util.ErrorConstants as Errors
import taxon_home.views.util.Util as Util
from get import GetAPI

def getImageMetadata(request):
    renderObj = WebServiceObject()
    if request.GET.has_key('id'):
        # the key for lookup and the image it is attached to
        imageKey = request.GET['id']
        fields = Util.getDelimitedList(request.GET, 'fields')
        getAPI = GetAPI(request.user, fields)
        try:
            renderObj = getAPI.getImageMetadata(imageKey)
        except Errors.WebServiceException as e:
            renderObj.setError(e)
    else:
        renderObj.setError(Errors.NO_IMAGE_KEY)
    
    return renderObj