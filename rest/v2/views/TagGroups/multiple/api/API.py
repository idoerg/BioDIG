import base.util.ErrorConstants as Errors
import base.util.Util as Util
from get import GetAPI
from post import PostAPI
import biodigWSC.swagger.decorators.Operations as Operations
import biodigWSC.swagger.decorators.Parameters as Params
import biodigWSC.swagger.decorators.Types as Types

'''
    Gets the information for a tag given its key
    
    @param request: Django Request object to be used to parse the query
'''
@Operations.Method(Operations.GET)
@Operations.Nickname('getTagGroups')
@Operations.Type('TagGroupSerializer')
@Params.Query('offset', Types.Integer)
@Params.Query('limit', Types.Integer)
@Params.Query('unlimited', Types.Boolean)
@Params.Query('fields', Types.String)
@Params.Query('lastModified', Types.Date)
@Params.Query('user', Types.String)
@Params.Query('image', Types.String)
@Params.Query('name', Types.String)
def getTagGroups(request):
    # read in optional parameters and initialize the API
    offset = Util.getInt(request.GET, 'offset', 0)
    limit = Util.getInt(request.GET, 'limit', 10)

    unlimited = request.GET.get('unlimited', False)
    fields = Util.getDelimitedList(request.GET, 'fields')
    
    getAPI = GetAPI(limit, offset, request.user, fields, unlimited)
    
    # read in parameters for limiting search
    lastModified = request.GET.get('lastModified', None)
    dateCreated = request.GET.get('dateCreated', None)
    user = Util.getDelimitedList(request.GET, 'user')
    image = Util.getDelimitedList(request.GET, 'image')
    name = Util.getDelimitedList(request.GET, 'name')
    
    return getAPI.getTagGroups(name, image, user, lastModified, dateCreated)
        

'''
    Creates a new tag and returns the newly created tag information
    
    @param request: Django Request object to be used to parse the query
'''
@Operation.Method(Operations.POST)
@Operation.Nickname('createTagGroup')
@Operations.Type('TagGroupSerializer')
@Params.Body('imageId', Types.Integer)
@Params.Body('name', Types.String)
@Params.Query('fields', Types.String)
def createTagGroup(request):
    imageKey = request.POST.get('imageId', None)
    if not imageKey:
        raise Errors.MISSING_PARAMETER.setCustom('imageId')
        
    # get the name
    name = request.POST.get('name', None)
    if not name:
        raise Errors.MISSING_PARAMETER.setCustom('name')  
    
    # get optional parameter
    fields = Util.getDelimitedList(request.POST, 'fields')
    
    postAPI = PostAPI(request.user, fields)
    return postAPI.createTagGroup(imageKey, name)
    
    
    
