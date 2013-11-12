from base.renderEngine.WebServiceObject import WebServiceObject
import base.util.Util as Util
from get import GetAPI

def getImageTags(request):
    renderObj = WebServiceObject()
    
    # read in crucial parameters
    tagGroupKey = request.GET.get('tagGroupId', None)
    imageKey = request.GET.get('imageId', None)
    
    # read in optional parameters and initialize the API
    offset = Util.getInt(request.GET, 'offset', 0)
    limit = Util.getInt(request.GET, 'limit', 10)
    unlimited = request.GET.get('unlimited', False)
    fields = Util.getDelimitedList(request.GET, 'fields')
    getAPI = GetAPI(limit, offset, request.user, fields, unlimited)
    
    if tagGroupKey:
        # the key for lookup and the image it is attached to
        renderObj = getAPI.getTagsByTagGroup(tagGroupKey, isKey=True)
    elif imageKey:
        # the key for lookup and the image it is attached to
        renderObj = getAPI.getTagsByImage(imageKey, isKey=True)
    else:
        # get all the tags
        renderObj = getAPI.getTags()
           
    return renderObj
