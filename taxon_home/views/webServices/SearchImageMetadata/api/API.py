from renderEngine.WebServiceObject import WebServiceObject
import taxon_home.views.util.ErrorConstants as Errors
import taxon_home.views.util.Util as Util
from get import GetAPI

def getImageMetadata(request):
    renderObj = WebServiceObject()
    if request.GET.has_key('imageKey'):
        # the key for lookup and the image it is attached to
        imageKey = request.GET['imageKey']
        fields = Util.getDelimitedList(request.GET, 'fields')
        
        getAPI = GetAPI(request.user, fields)
        renderObj = getAPI.getImageMetadata(imageKey)                
    else:
        renderObj.setError(Errors.NO_IMAGE_KEY)
    
    return renderObj