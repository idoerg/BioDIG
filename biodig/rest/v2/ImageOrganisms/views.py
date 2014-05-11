from biodig.base.exceptions import BadRequestException
from rest_framework.views import APIView
from rest_framework.response import Response

from biodig.rest.v2.ImageOrganisms.forms import MultiGetForm, PostForm, DeleteForm, SingleGetForm

class ImageOrganismList(APIView):
    '''
       Class for rendering the view for creating ImageOrganisms and
       searching through the ImageOrganisms.
    '''

    def get(self, request, image_id):
        '''
            Method for getting multiple ImageOrganisms either through search
            or general listing.
        '''
        params = dict((key, val) for key, val in request.QUERY_PARAMS.iteritems())
        params['image_id'] = image_id
        form = MultiGetForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))

    def post(self, request, image_id):
        '''
            Method for creating a new ImageOrganism.
        '''
        params = dict((key, val) for key, val in request.DATA.iteritems())
        params.update(request.QUERY_PARAMS)
        params['image_id'] = image_id
        form = PostForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))


class ImageOrganismSingle(APIView):
    '''
       Class for rendering the view for getting a Organim, deleting a ImageOrganism
       and updating a ImageOrganism.
    '''

    def get(self, request, image_id, organism_id):
        '''
            Method for getting an ImageOrganism.
        '''
        params = dict((key, val) for key, val in request.QUERY_PARAMS.iteritems())
        params['image_id'] = image_id
        params['organism_id'] = organism_id
        form = SingleGetForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))

    def delete(self, request, image_id, organism_id):
        '''
            Method for deleting an ImageOrganism.
        '''
        params = dict((key, val) for key, val in request.QUERY_PARAMS.iteritems())
        params['image_id'] = image_id
        params['organism_id'] = organism_id
        form = DeleteForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))
