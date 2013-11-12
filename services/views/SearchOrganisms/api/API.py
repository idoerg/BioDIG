import base.util.Util as Util
from get import GetAPI

def getOrganisms(request):
    # get the list of organisms (base on comma delimited list)
    organisms = Util.getDelimitedList(request.GET, 'organisms')

    # optional parameters
    fields = Util.getDelimitedList(request.GET, 'fields')

    getAPI = GetAPI(request.user, fields)
    
    return getAPI.getOrganisms(organisms)
