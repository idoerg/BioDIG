from taxon_home.models import Picture, PictureDefinitionTag
from renderEngine.WebServiceObject import WebServiceArray, WebServiceObject, LimitDict
from renderEngine.WebServiceException import WebServiceException
from taxon_home.views.webServices.Images.api.get import GetAPI as ImageMetadataAPI


class GetAPI:
    def __init__(self, limit=10, offset=0, user=None, fields=None, unlimited=False):
        self.user = user
        self.fields = fields
        self.limit = limit
        self.offset = offset
        self.unlimited = unlimited


