import base.util.ErrorConstants as Errors
import base.util.Util as Util
from get import GetAPI

def getImageMetadata(request):
    #optional parameters
    offset = Util.getInt(request.GET, 'offset', 0)
    limit = Util.getInt(request.GET, 'limit', 10)
    unlimited = request.GET.get('unlimited', False)
    fields = Util.getDelimitedList(request.GET, 'fields')

    getAPI = GetAPI(limit, offset, request.user, fields, unlimited)
    if request.GET.has_key('by'):
        by = request.GET['by']        
        if by == 'organism':
            # required paramaters
            organismIds = Util.getDelimitedList(request.GET, 'organismId')
            return getAPI.getImageMetadataByOrganism(organismIds)
        else:
            raise Errors.INVALID_PARAMETER.setCustom('by')
    else:
        return getAPI.getImageMetadata()
