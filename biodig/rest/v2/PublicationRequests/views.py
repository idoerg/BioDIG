from biodig.base.exceptions import BadRequestException
from rest_framework.views import APIView
from rest_framework.response import Response

from biodig.rest.v2.PublicationRequests.forms import MultiGetForm, PreviewForm, PostForm, PutForm, DeleteForm, SingleGetForm

class PublicationRequestList(APIView):
    '''
       Class for rendering the view for creating PublicationRequests and
       searching through the PublicationRequests.
    '''

    def get(self, request):
        '''
            Method for getting multiple PublicationRequests either through search
            or general listing.
        '''
        params = dict((key, val) for key, val in request.QUERY_PARAMS.iteritems())
        form = MultiGetForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))

    def post(self, request):
        '''
            Method for creating a new PublicationRequest.
        '''
        params = dict((key, val) for key, val in request.DATA.iteritems())
        params.update(request.QUERY_PARAMS)
        form = PostForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))


class PublicationRequestSingle(APIView):
    '''
       Class for rendering the view for getting a PublicationRequest, deleting a PublicationRequest
       and updating a PublicationRequest.
    '''

    def get(self, request, publication_request_id):
        '''
            Method for getting an PublicationRequest.
        '''
        params = dict((key, val) for key, val in request.QUERY_PARAMS.iteritems())
        params['publication_request_id'] = publication_request_id
        form = SingleGetForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))

    def put(self, request, publication_request_id):
        '''
            Method for updating a PublicationRequest's information.
        '''
        params = dict((key, val) for key, val in request.DATA.iteritems())
        params['publication_request_id'] = publication_request_id
        form = PutForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))

    def delete(self, request, publication_request_id):
        '''
            Method for canceling an PublicationRequest.
        '''
        params = dict((key, val) for key, val in request.QUERY_PARAMS.iteritems())
        params['publication_request_id'] = publication_request_id
        form = DeleteForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))

class PublicationRequestPreview(APIView):
    '''
       Class for rendering the view for getting a preview of a PublicationRequest.
    '''

    def get(self, request, publication_request_id):
        '''
            Method for getting an PublicationRequest's preview.
        '''
        params = dict((key, val) for key, val in request.QUERY_PARAMS.iteritems())
        params['publication_request_id'] = publication_request_id
        form = PreviewForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))
