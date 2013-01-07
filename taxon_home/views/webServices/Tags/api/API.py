import taxon_home.views.util.ErrorConstants as Errors
import taxon_home.views.util.Util as Util
import simplejson as json
from get import GetAPI
from post import PostAPI
from put import PutAPI
from delete import DeleteAPI

'''
    Gets the information for a tag given its key
    
    @param request: Django Request object to be used to parse the query
'''
def getTag(request):
    # read in crucial parameters
    tagKey = request.GET.get('id', None)
    
    # read in optional parameters and initialize the API
    fields = Util.getDelimitedList(request.GET, 'fields')
    getAPI = GetAPI(request.user, fields)

    if not tagKey:
        raise Errors.NO_TAG_KEY
    
    # the key for lookup and the image it is attached to
    return getAPI.getTag(tagKey)

'''
    Updates the tag information as posted and returns the newly updated tag information
    
    @param request: Django Request object to be used to parse the query
'''
def updateTag(request):
    # read in the crucial parameters
    tagKey = request.PUT.get('id', None)
    if not tagKey:
        raise Errors.MISSING_PARAMETER.setCustom('id')
    
    points = request.PUT.get('points', None)
    if points:
        try:
            points = json.loads(points)
        except ValueError:
            raise Errors.INVALID_SYNTAX.setCustom('points')
    else:
        raise Errors.MISSING_PARAMETER.setCustom('points')
    
    color = request.PUT.get('color', None)
    if color:
        try:
            color = json.loads(color)
        except ValueError:
            color = Util.getDelimitedList(request.PUT, 'color')
    else:
        raise Errors.MISSING_PARAMETER.setCustom('color')
    
    description = request.PUT.get('description', None)
    if description:
        raise Errors.MISSING_PARAMETER.setCustom('description')
    
    # read in optional parameters and initialize the API
    fields = Util.getDelimitedList(request.PUT, 'fields')
    putAPI = PutAPI(request.user, fields)
    
    return putAPI.updateTag(tagKey, points, description, color)

'''
    Creates a new gene link and returns the representation of the newly created gene link.
    
    @param request: Django Request object to be used to parse the query
'''
def createTag(request):
    # get tagId for new gene link
    tagId = request.POST.get('tagId', None)
    
    if not tagId:
        raise Errors.NO_TAG_KEY
    
    # find name or uniquename
    name = request.POST.get('name', None)
    uniquename = request.POST.get('uniquename', None)
    organismId = request.POST.get('organismId', None)
    
    # read in optional parameters and initialize the API
    fields = Util.getDelimitedList(request.POST, 'fields')
    
    if not (uniquename or (name and organismId)):
        if not uniquename:
            raise Errors.MISSING_PARAMETER.setCustom('uniquename')
        else:
            raise Errors.INVALID_SYNTAX.setCustom('name and organismId required')
        
    postAPI = PostAPI(request.user, fields)
    return postAPI.createGeneLink(name, uniquename, organismId)

'''
    Deletes a tag and returns the information for the tag that was deleted
'''
def deleteTag(request):
    geneLinkKey = request.DELETE.get('id', None)
    
    if not geneLinkKey:
        raise Errors.MISSING_PARAMETER.setCustom('id')
    
    # get optional parameter
    fields = Util.getDelimitedList(request.DELETE, 'fields')
    
    deleteAPI = DeleteAPI(request.user, fields)
    return deleteAPI.deleteGeneLink(geneLinkKey)
    
    
    