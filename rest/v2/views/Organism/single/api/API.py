import base.util.ErrorConstants as Errors
import base.util.Util as Util
from get import GetAPI
from put import PutAPI
from delete import DeleteAPI

'''
    Gets the information for a tag given its key
    
    @param request: Django Request object to be used to parse the query
    @param key: Numeric key for the tag group being asked for
'''
def getOrganism(request, key):
    # read in optional parameters and initialize the API
    fields = Util.getDelimitedList(request.GET, 'fields')
    getAPI = GetAPI(request.user, fields)

    if not key:
        raise Errors.NO_TAG_GROUP_KEY
    
    # the key for lookup and the image it is attached to
    return getAPI.getOrganism(key)

'''
    Updates the tag group information as posted and returns the newly updated tag group information
    
    @param request: Django Request object to be used to parse the query
    @param key: Numeric key for the tag group that should be edited
'''
def updateOrganism(request, key):
    if not key:
        raise Errors.NO_TAG_GROUP_KEY
    
    name = request.PUT.get('name', None)
    
    # read in optional parameters and initialize the API
    fields = Util.getDelimitedList(request.PUT, 'fields')
    putAPI = PutAPI(request.user, fields)
    
    if not name:
        raise Errors.NOT_MODIFIED
    
    return putAPI.updateOrganism(key, name)

'''
    Deletes a tag group and returns the information for the tag group that was deleted
    
    @param request: Django Request object to be used to parse the query
    @param key: Numeric key for the tag group that should be deleted
'''
def deleteOrganism(request, key):
    
    if not key:
        raise Errors.NO_TAG_GROUP_KEY
    
    # get optional parameter
    fields = Util.getDelimitedList(request.DELETE, 'fields')
    
    deleteAPI = DeleteAPI(request.user, fields)
    return deleteAPI.deleteOrganism(key)
    
    
    
