from django.shortcuts import get_object_or_404, render_to_response
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from mycoplasma_home.models import Picture
from django.core.files.uploadedfile import UploadedFile
from django.core.files import File

#importing json parser to generate jQuery plugin friendly json response
from django.utils import simplejson

#for generating thumbnails
#sorl-thumbnails must be installed and properly configured
from sorl.thumbnail import get_thumbnail

#importing PIL Image for conversion of certain image types
from PIL import Image as PILImage
import os
import cStringIO
import hashlib


from django.views.decorators.csrf import csrf_exempt

import logging
log = logging


def handleUpload(file):
    imagefile  = cStringIO.StringIO(file.read())
    thumbImage = PILImage.open(imagefile)  

    thumbfile = cStringIO.StringIO()
    thumbImage.save(thumbfile, "PNG")

    filename = hashlib.md5(thumbfile.getvalue()).hexdigest()+'.png'

    thumbfile = open(os.path.join('/tmp',filename), 'w')
    thumbImage.save(thumbfile,'PNG')
    thumbfile = open(os.path.join('/tmp',filename), 'r')
    content = File(thumbfile)

    return (UploadedFile(content), filename);

@csrf_exempt
def multiuploader_delete(request, pk):
    """
    View for deleting photos with multiuploader AJAX plugin.
    made from api on:
    https://github.com/blueimp/jQuery-File-Upload
    """
    if request.method == 'POST':
        log.info('Called delete image. image id='+str(pk))
        image = get_object_or_404(modelsImage, pk=pk)
        image.delete()
        log.info('DONE. Deleted photo id='+str(pk))
        return HttpResponse(str(pk))
    else:
        log.info('Received not POST request to delete image view')
        return HttpResponseBadRequest('Only POST accepted')

@csrf_exempt
def multiuploader(request):
    """
    Main Multiuploader module
    """
    if request.method == 'POST' and request.user.is_authenticated():
        log.info('received POST to main multiuploader view')
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')
        
        #getting file data for farther manipulations
        file = request.FILES[u'files[]']
        
        (wrapped_file, filename) = handleUpload(file);
        #filename = wrapped_file.name
        file_size = wrapped_file.file.size
        # log.info ('Got file: "%s"' % str(filename))

        #writing file manually into model
        #because we don't need form of any type.
        image = Picture()
        image.imageName = wrapped_file.file
        image.user = request.user
        image.isPrivate = True
        image.save()
        log.info('File saving done')

        #getting thumbnail url using sorl-thumbnail
        im = get_thumbnail(image, "80x80", quality=50)
        thumb_url = im.url

        #settings imports
        try:
            file_delete_url = settings.MULTI_FILE_DELETE_URL + '/'
            file_url = settings.MEDIA_URL + image.imageName.name
        except AttributeError:
            file_delete_url = 'multi_delete/'
            file_url = 'multi_image/'+image.key_data+'/'

        #generating json response array
        result = []
        result.append({
           "name" : filename, 
           "size" : file_size, 
           "url" : file_url,
           "thumbnail_url" : thumb_url,
           "delete_url" : file_delete_url + ' ?imageKey=' + str(image.pk), 
           "delete_type" : "POST"
        })
        response_data = simplejson.dumps(result)
        
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)
    else: #GET
        return HttpResponse('Only POST accepted')

