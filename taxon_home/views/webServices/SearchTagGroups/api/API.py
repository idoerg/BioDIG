from renderEngine.WebServiceObject import WebServiceObject
import taxon_home.views.util.Util as Util
from get import GetAPI

def getImageTagGroups(request):
    renderObj = WebServiceObject()
    
    # the key for lookup and the image it is attached to
    imageKey = request.GET.get('imageId', None)
    offset = Util.getInt(request.GET, 'offset', 0)
    limit = Util.getInt(request.GET, 'limit', 10)

    unlimited = request.GET.get('unlimited', False)
    fields = Util.getDelimitedList(request.GET, 'fields')
    
    getAPI = GetAPI(limit, offset, request.user, fields, unlimited)
    
    if imageKey:
        renderObj = getAPI.getTagGroupsByImage(imageKey)
    else:
        renderObj = getAPI.getTagGroups()
        
    return renderObj
    
    