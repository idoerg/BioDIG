import taxon_home.views.util.ErrorConstants as Errors
import taxon_home.views.util.Util as Util
from get import GetAPI
from put import PutAPI
from delete import DeleteAPI

'''
    Gets the information for a tag given its key
    
    @param request: Django Request object to be used to parse the query
    @param key: Numeric key for the tag group being asked for
'''
def getOrganism(request, key):
    if not key:
        raise Errors.MISSING_PARAMETER.setCustom('id')
    
    # read in optional parameters and initialize the API
    fields = Util.getDelimitedList(request.GET, 'fields')
    getAPI = GetAPI(request.user, fields)
    
    # the key for lookup and the image it is attached to
    return getAPI.getOrganism(key)

'''
    Updates the tag group information as posted and returns the newly updated tag group information
    
    @param request: Django Request object to be used to parse the query
    @param key: Numeric key for the tag group that should be edited
'''
def updateOrganism(request, key):
    if not key:
        raise Errors.MISSING_PARAMETER.setCustom('id')
    
    abbreviation = request.PUT.get('abbreviation', None)
    genus = request.PUT.get('genus', None)
    species = request.PUT.get('species', None)
    commonName = request.PUT.get('commonName', None)
    comment = request.PUT.get('comment', None)
    
    # read in optional parameters and initialize the API
    fields = Util.getDelimitedList(request.PUT, 'fields')
    putAPI = PutAPI(request.user, fields)
    
    if not (abbreviation or genus or species or commonName or comment):
        raise Errors.NOT_MODIFIED
    
    return putAPI.updateOrganism(key, abbreviation, genus, species, commonName, comment)

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
    return deleteAPI.deleteTagGroup(key)
    
    
    