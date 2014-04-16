from biodig.base.exceptions import BadRequestException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from biodig.rest.v2.Users.forms import MultiGetForm, PostForm, PutForm, DeleteForm, SingleGetForm

class UserList(APIView):
    permission_classes = (AllowAny,) # a POST by an unknown user will allow them to signup

    '''
       Class for rendering the view for creating Users and
       searching through the Users.
    '''

    def get(self, request):
        '''
            Method for getting multiple Users either through search
            or general listing.
        '''
        params = { key : val for key, val in request.QUERY_PARAMS.iteritems() }
        form = MultiGetForm(params)

        if not form.is_valid():
            raise BadRequestException(detail=form.errors)

        return Response(form.submit(request))

    def post(self, request):
        '''
            Method for creating a new User.
        '''
        params = { key : val for key, val in request.DATA.iteritems() }
        params.update(request.QUERY_PARAMS)
        form = PostForm(params)

        if not form.is_valid():
            raise BadRequestException(detail=form.errors)

        return Response(form.submit(request))


class UserSingle(APIView):
    '''
       Class for rendering the view for getting a User, deleting a User
       and updating a User.
    '''

    def get(self, request, user_id):
        '''
            Method for getting multiple Users either through search
            or general listing.
        '''
        params = { key : val for key, val in request.QUERY_PARAMS.iteritems() }
        params['user_id'] = user_id
        form = SingleGetForm(params)

        if not form.is_valid():
            raise BadRequestException(detail=form.errors)

        return Response(form.submit(request))

    def put(self, request, user_id):
        '''
            Method for updating a User's information.
        '''
        params = { key : val for key, val in request.DATA.iteritems() }
        params.update(request.DATA)
        params['user_id'] = user_id
        form = PutForm(params)

        if not form.is_valid():
            raise BadRequestException(detail=form.errors)

        return Response(form.submit(request))

    def delete(self, request, user_id):
        '''
            Method for deleting a a User.
        '''
        params = { key : val for key, val in request.QUERY_PARAMS.iteritems() }
        params['user_id'] = user_id
        form = DeleteForm(params)

        if not form.is_valid():
            raise BadRequestException(detail=form.errors)

        return Response(form.submit(request))
