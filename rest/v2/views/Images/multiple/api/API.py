from base.renderEngine.WebServiceObject import WebServiceObject
import base.util.ErrorConstants as Errors
import base.util.Util as Util
from get import GetAPI
from post import PostAPI

def getImages(request):
    renderObj = WebServiceObject()
    if request.GET.has_key('id'):
        # the key for lookup and the image it is attached to
        imageKey = request.GET['id']
        fields = Util.getDelimitedList(request.GET, 'fields')
        getAPI = GetAPI(request.user, fields)
        try:
            renderObj = getAPI.getImageMetadata(imageKey)
        except Errors.WebServiceException as e:
            renderObj.setError(e)
    else:
        renderObj.setError(Errors.NO_IMAGE_KEY)
    
    return renderObj

def createImage(request):
    renderObj = WebServiceObject()
    
    # these should overwrite current metadata
    image = request.FILES.get('image', None)
    description = request.POST.get('description', None)
    altText = request.POST.get('altText', None)
    organisms = Util.getDelimitedList(request.POST, 'organisms')
    fields = Util.getDelimitedList(request.POST, 'fields')
    
    if image:
        postAPI = PostAPI(request.user, fields)
        renderObj = postAPI.createImageMetadata(image, description, altText, organisms)
    else:
        raise Errors.MISSING_PARAMETER.setCustom('image')
    
    return renderObj

