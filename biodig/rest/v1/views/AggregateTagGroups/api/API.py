import biodig.base.util.Util as Util
import biodig.base.util.ErrorConstants as Errors
from get import GetAPI

'''
    Gets the information for a tag given its key
    
    @param request: Django Request object to be used to parse the query
'''
def getTagGroup(request):
    # read in crucial parameters
    tagGroupKey = request.GET.get('id', None)
    
    # read in optional parameters and initialize the API
    fields = Util.getDelimitedList(request.GET, 'fields')
    getAPI = GetAPI(request.user, fields)

    if not tagGroupKey:
        raise Errors.NO_TAG_GROUP_KEY
    
    # the key for lookup and the image it is attached to
    return getAPI.getTagGroup(tagGroupKey)
    
    
