from biodig.base.exceptions import BadRequestException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from biodig.rest.beetles.Orthologs.forms import MultiGetForm, SingleGetForm

class OrthologList(APIView):
    permission_classes = (AllowAny, )

    '''
       Class for rendering the view for searching through the Orthologs.
    '''

    def get(self, request):
        '''
            Method for getting multiple Orthologs either through search
            or general listing.
        '''
        params = dict((key, val) for key, val in request.QUERY_PARAMS.iteritems())
        form = MultiGetForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))

class OrthologSingle(APIView):
    permission_classes = (AllowAny, )
    
    '''
       Class for rendering the view for getting a Ortholog.
    '''
    def get(self, request, TC_id):
        '''
            Method for getting sigle ortholog list
        '''
        params = dict((key, val) for key, val in request.QUERY_PARAMS.iteritems())
        params['TC_id'] = TC_id
        form = SingleGetForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))


