'''
	Application for the Images Page of the DOME
	URL: /images

	Author: Andrew Oberlin
	Date: July 23, 2012
'''
from biodig.base.models import Image
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.core.servers.basehttp import FileWrapper
import os

'''
	Adds a prefix check on user permissions before serving media files
'''
def renderAction(request, *args, **kwargs):
	authorized = False
	filename = os.path.join(settings.MEDIA_ROOT, query)

	# check for thumbnail
	thumbnailCheck = len(request.path_info.split(settings.MEDIA_URL)[1].split('thumbnails/')) > 1

	if request.user and request.user.is_authenticated():
		if request.user.is_staff:
			authorized = True
		else:
			if thumbnailCheck:
				authorized = Image.objects.get(thumbnail=request.path_info).readPermissions(request.user)
			else:
				authorized = Image.objects.get(imageName=request.path_info).readPermissions(request.user)
	else:
		try:
			if thumbnailCheck:
				authorized = not Image.objects.get(thumbnail=request.path_info).isPrivate
			else:
				authorized = not Image.objects.get(imageName=request.path_info).isPrivate
		except Exception as e:
			return HttpResponse("Error: " + str(e) + " for query: " + query)
			#return HttpResponseNotFound()

	if authorized:
		try:
			response = HttpResponse(FileWrapper(file(filename)), mimetype="image/png")
			response['Content-Length'] = os.path.getsize(filename)
			return response
		except Exception:
			return HttpResponseNotFound()
	else:
		return HttpResponseNotFound()
