import taxon_home.views.util.ErrorConstants as Errors
import taxon_home.views.util.Util as Util
from get import GetAPI
from put import PutAPI
from delete import DeleteAPI
import json

'''
    Gets the information for a tag given its key
    
    @param request: Django Request object to be used to parse the query
    @param key: Numeric key for the tag group being asked for
'''
def getTag(request, key):
    # read in optional parameters and initialize the API
    fields = Util.getDelimitedList(request.GET, 'fields')
    getAPI = GetAPI(request.user, fields)

    if not key:
        raise Errors.NO_TAG_KEY
    
    # the key for lookup and the image it is attached to
    return getAPI.getTag(key)

'''
    Updates the tag group information as posted and returns the newly updated tag group information
    
    @param request: Django Request object to be used to parse the query
    @param key: Numeric key for the tag group that should be edited
'''
def updateTag(request, key):
    # read in the crucial parameters    
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
    
    name = request.PUT.get('name', None)
    if not name:
        raise Errors.MISSING_PARAMETER.setCustom('name')
    
    # read in optional parameters and initialize the API
    fields = Util.getDelimitedList(request.PUT, 'fields')
    putAPI = PutAPI(request.user, fields)
    
    return putAPI.updateTag(key, points, name, color)

'''
    Deletes a tag group and returns the information for the tag group that was deleted
    
    @param request: Django Request object to be used to parse the query
    @param key: Numeric key for the tag group that should be deleted
'''
def deleteTag(request, key):
    
    if not key:
        raise Errors.NO_TAG_GROUP_KEY
    
    # get optional parameter
    fields = Util.getDelimitedList(request.DELETE, 'fields')
    
    deleteAPI = DeleteAPI(request.user, fields)
    return deleteAPI.deleteTagGroup(key)
    
    
    