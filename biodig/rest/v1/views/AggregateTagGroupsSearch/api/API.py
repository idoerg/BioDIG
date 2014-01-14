import biodig.base.util.Util as Util
from get import GetAPI

def getAggregateTagGroups(request):
    # the key for lookup and the image it is attached to
    imageKey = request.GET.get('imageId', None)
    offset = Util.getInt(request.GET, 'offset', 0)
    limit = Util.getInt(request.GET, 'limit', 10)

    unlimited = request.GET.get('unlimited', False)
    fields = Util.getDelimitedList(request.GET, 'fields')
    
    getAPI = GetAPI(limit, offset, request.user, fields, unlimited)
    
    if imageKey:
        return getAPI.getAggregateTagGroupsByImage(imageKey)
    else:
        return getAPI.getAggregateTagGroups()
    
    
