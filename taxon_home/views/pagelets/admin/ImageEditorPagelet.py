'''
    Pagelet for the Image Editor which is both an admin
    and a public application

    Author: Andrew Oberlin
    Date: August 5, 2012
'''

from renderEngine.PageletBase import PageletBase
import simplejson as json
from taxon_home.views.webServices.SearchGeneLinks.api.get import GetAPI as GeneLinkAPI
from taxon_home.views.webServices.SearchTags.api.get import GetAPI as TagAPI
from taxon_home.views.webServices.SearchTagGroups.api.get import GetAPI as TagGroupAPI
from taxon_home.views.webServices.ImageMetadata.api.get import GetAPI as ImageMetadataAPI
from taxon_home.models import Picture
from django.core.exceptions import ObjectDoesNotExist

class ImageEditorPagelet(PageletBase):
    '''
        Renders the center of the home page        
    
        Params: request -- the Django request object with the POST & GET args
        
        Returns: Dictionary of arguments for rendering this pagelet
    '''
    def doProcessRender(self, request):
        self.setLayout('admin/imageEditor.html')
        try:
            imageKey = request.GET.get('imageId', None)
            if (imageKey):
                image = Picture.objects.get(pk__exact=imageKey)
                
                # initialize tagging APIs
                tagGroupAPI = TagGroupAPI(unlimited=True)
                tagAPI = TagAPI(unlimited=True)
                geneLinkAPI = GeneLinkAPI(unlimited=True)
                
                tagGroups = tagGroupAPI.getTagGroupsByImage(image, False).getObject()
                
                for group in tagGroups:
                    tags = tagAPI.getTagsByTagGroup(group['id']).getObject()
                    for tag in tags:
                        geneLinks = geneLinkAPI.getGeneLinksByTag(tag['id']).getObject()
                        tag['geneLinks'] = geneLinks
                    group['tags'] = tags
                    
                # initialize image metadata API
                imageMetadataAPI = ImageMetadataAPI(request.user)
                imageMetadata = imageMetadataAPI.getImageMetadata(image, isKey=False).getObject()
        
                return {
                    'imageMetadata' : json.dumps(imageMetadata),
                    'tagGroups' : json.dumps(tagGroups),
                    'image' : image
                }
            else:
                self.setLayout('public/404Media.html')
                return {}
        except ObjectDoesNotExist:
            self.setLayout('public/404Media.html')
            return {}
        except KeyError:
            self.setLayout('public/404Media.html')
            return {}
