from biodig.base.exceptions import BadRequestException
from rest_framework.views import APIView
from rest_framework.response import Response

from biodig.rest.v2.Tags.forms import MultiGetForm, PostForm, PutForm, DeleteForm, SingleGetForm

class TagList(APIView):
    '''
       Class for rendering the view for creating Tags and
       searching through the Tags.
    '''

    def get(self, request):
        '''
            Method for getting multiple Tags either through search
            or general listing.
        '''
        form = MultiGetForm(request.QUERY_PARAMS)
        
        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))

    def post(self, request):
        '''
            Method for creating a new Tag.
        '''
        params = { key : val for key, val in request.DATA }
        params.update(request.QUERY_PARAMS)
        form = PostForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))


class TagSingle(APIView):
    '''
       Class for rendering the view for getting a Tag, deleting a Tag
       and updating a Tag. 
    '''

    def get(self, request, tag_id):
        '''
            Method for getting multiple Tags either through search
            or general listing.
        '''
        params = { key : val for key, val in request.QUERY_PARAMS }
        params['tag_id'] = tag_id
        form = SingleGetForm(params)
        
        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))

    def put(self, request, tag_id):
        '''
            Method for updating a TagGroup's information.
        '''
        params = { key : val for key, val in request.DATA }
        params.update(request.DATA)
        params['tag_id'] = tag_id
        form = PutForm(params)
        
        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))

    def delete(self, request, tag_id):
        '''
            Method for deleting a a TagGroup.
        '''
        params = { key : val for key, val in request.QUERY_PARAMS }
        params['tag_id'] = tag_id
        form = DeleteForm(params)
        
        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))
