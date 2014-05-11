from biodig.base.exceptions import BadRequestException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from biodig.rest.v2.Cvterms.forms import MultiGetForm, SingleGetForm

class CvtermList(APIView):
    permission_classes = (AllowAny, )

    '''
       Class for rendering the view for searching through the Cvterms.
    '''

    def get(self, request, cv):
        '''
            Method for getting multiple Cvterms either through search
            or general listing.
        '''
        params = dict((key, val) for key, val in request.QUERY_PARAMS.iteritems())
        params['cv'] = cv
        form = MultiGetForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))


class CvtermSingle(APIView):
    permission_classes = (AllowAny, )

    '''
       Class for rendering the view for getting a Cvterm.
    '''

    def get(self, request, cv, Cvterm_id):
        '''
            Method for getting multiple Cvterms either through search
            or general listing.
        '''
        params = dict((key, val) for key, val in request.QUERY_PARAMS.iteritems())
        params['Cvterm_id'] = Cvterm_id
        params['cv'] = cv
        form = SingleGetForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))
