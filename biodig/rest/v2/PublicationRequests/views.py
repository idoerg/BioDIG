from biodig.base.exceptions import BadRequestException
from rest_framework.views import APIView
from rest_framework.response import Response

from biodig.rest.v2.PublicationRequests.forms import MultiGetForm, PostForm, DeleteForm, SingleGetForm

class PublicationRequestList(APIView):
    '''
       Class for rendering the view for creating PublicationRequests and
       searching through the PublicationRequests.
    '''

    def get(self, request, image_id):
        '''
            Method for getting multiple PublicationRequests either through search
            or general listing.
        '''
        params = { key : val for key, val in request.QUERY_PARAMS.iteritems() }
        params['image_id'] = image_id
        form = MultiGetForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))

    def post(self, request, image_id):
        '''
            Method for creating a new PublicationRequest.
        '''
        params = { key : val for key, val in request.DATA.iteritems() }
        params.update(request.QUERY_PARAMS)
        params['image_id'] = image_id
        form = PostForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))


class PublicationRequestSingle(APIView):
    '''
       Class for rendering the view for getting a Organim, deleting a PublicationRequest
       and updating a PublicationRequest.
    '''

    def get(self, request, image_id, organism_id):
        '''
            Method for getting an PublicationRequest.
        '''
        params = { key : val for key, val in request.QUERY_PARAMS.iteritems() }
        params['image_id'] = image_id
        params['organism_id'] = organism_id
        form = SingleGetForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))

    def delete(self, request, image_id, organism_id):
        '''
            Method for deleting an PublicationRequest.
        '''
        params = { key : val for key, val in request.QUERY_PARAMS.iteritems() }
        params['image_id'] = image_id
        params['organism_id'] = organism_id
        form = DeleteForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))
