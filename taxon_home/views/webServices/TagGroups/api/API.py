import taxon_home.views.util.ErrorConstants as Errors
import taxon_home.views.util.Util as Util
from get import GetAPI
from post import PostAPI
from put import PutAPI
from delete import DeleteAPI

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

'''
    Updates the tag information as posted and returns the newly updated tag information
    
    @param request: Django Request object to be used to parse the query
'''
def updateTagGroup(request):
    # read in the crucial parameters
    tagGroupKey = request.PUT.get('id', None)
    if not tagGroupKey:
        raise Errors.MISSING_PARAMETER.setCustom('id')
    
    name = request.PUT.get('name', None)
    
    # read in optional parameters and initialize the API
    fields = Util.getDelimitedList(request.PUT, 'fields')
    putAPI = PutAPI(request.user, fields)
    
    if not name:
        raise Errors.NOT_MODIFIED
    
    return putAPI.updateTagGroup(tagGroupKey, name)
        

'''
    Creates a new tag and returns the newly created tag information
    
    @param request: Django Request object to be used to parse the query
'''
def createTagGroup(request):
    imageKey = request.POST.get('imageId', None)
    if not imageKey:
        raise Errors.MISSING_PARAMETER.setCustom('imageId')
        
    # get the description
    name = request.POST.get('name', None)
    if not name:
        raise Errors.MISSING_PARAMETER.setCustom('name')  
    
    # get optional parameter
    fields = Util.getDelimitedList(request.POST, 'fields')
    
    postAPI = PostAPI(request.user, fields)
    return postAPI.createTagGroup(imageKey, name)

'''
    Deletes a tag and returns the information for the tag that was deleted
'''
def deleteTagGroup(request):
    tagGroupKey = request.DELETE.get('id', None)
    
    if not tagGroupKey:
        raise Errors.MISSING_PARAMETER.setCustom('id')
    
    # get optional parameter
    fields = Util.getDelimitedList(request.DELETE, 'fields')
    
    deleteAPI = DeleteAPI(request.user, fields)
    return deleteAPI.deleteTagGroup(tagGroupKey)
    
    
    