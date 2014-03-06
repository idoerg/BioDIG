'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for Images.
    
    Created on March 5, 2013

    @author: Andrew Oberlin
'''
from biodig.base.exceptions import BadRequestException
from rest_framework.views import APIView
from rest_framework.response import Response

from biodig.rest.v2.Images.forms import MultiGetForm, PostForm, PutForm, DeleteForm, SingleGetForm

class ImagesList(APIView):
    '''
       Class for rendering the view for creating Images and
       searching through the Images.
    '''

    def get(self, request):
        '''
            Method for getting multiple Images either through search
            or general listing.
        '''
        form = MultiGetForm(request.QUERY_PARAMS)
        
        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))

    def post(self, request):
        '''
            Method for creating a new Image.
        '''
        params = { key : val for key, val in request.DATA.iteritems() }
        params.update(request.QUERY_PARAMS)
        form = PostForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))


class ImageSingle(APIView):
    '''
       Class for rendering the view for getting a Image, deleting a Image
       and updating a Image. 
    '''

    def get(self, request, image_id):
        '''
            Method for getting multiple Images either through search
            or general listing.
        '''
        params = { key : val for key, val in request.QUERY_PARAMS.iteritems() }
        params['image_id'] = image_id
        form = SingleGetForm(params)
        
        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))

    def put(self, request, image_id, tag_group_id):
        '''
            Method for updating a Image's information.
        '''
        params = { key : val for key, val in request.DATA.iteritems() }
        params.update(request.DATA)
        params['image_id'] = image_id
        form = PutForm(params)
        
        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))

    def delete(self, request, image_id):
        '''
            Method for deleting a a Image.
        '''
        params = { key : val for key, val in request.QUERY_PARAMS.iteritems() }
        params['image_id'] = image_id
        form = DeleteForm(params)
        
        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))
