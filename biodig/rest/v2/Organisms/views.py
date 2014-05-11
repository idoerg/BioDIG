from biodig.base.exceptions import BadRequestException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from biodig.rest.v2.Organisms.forms import MultiGetForm, SingleGetForm

class OrganismList(APIView):

    '''
       Class for rendering the view for searching through the Organisms.
    '''

    def get(self, request):
        '''
            Method for getting multiple Organisms either through search
            or general listing.
        '''
        params = dict((key, val) for key, val in request.QUERY_PARAMS.iteritems())
        form = MultiGetForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))


class OrganismSingle(APIView):
    '''
       Class for rendering the view for getting a Organism.
    '''

    def get(self, request, user_id):
        '''
            Method for getting multiple Organisms either through search
            or general listing.
        '''
        params = dict((key, val) for key, val in request.QUERY_PARAMS.iteritems())
        params['organism_id'] = organism_id
        form = SingleGetForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))
