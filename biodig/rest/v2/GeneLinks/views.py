from biodig.base.exceptions import BadRequestException
from rest_framework.views import APIView
from rest_framework.response import Response

from biodig.rest.v2.GeneLinks.forms import MultiGetForm, PostForm, DeleteForm, SingleGetForm

class GeneLinkList(APIView):
    '''
       Class for rendering the view for creating GeneLinks and
       searching through the GeneLinks.
    '''

    def get(self, request, image_id, tag_group_id, tag_id):
        '''
            Method for getting multiple GeneLinks either through search
            or general listing.
        '''
        params = dict((key, val) for key, val in request.QUERY_PARAMS.iteritems())
        params['image_id'] = image_id
        params['tag_group_id'] = tag_group_id
        params['tag_id'] = tag_id
        form = MultiGetForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))

    def post(self, request, image_id, tag_group_id, tag_id):
        '''
            Method for creating a new GeneLink.
        '''
        params = dict((key, val) for key, val in request.DATA.iteritems())
        params.update(request.QUERY_PARAMS)
        params['image_id'] = image_id
        params['tag_group_id'] = tag_group_id
        params['tag_id'] = tag_id
        form = PostForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))


class GeneLinkSingle(APIView):
    '''
       Class for rendering the view for getting a GeneLink, deleting a GeneLink
       and updating a GeneLink.
    '''

    def get(self, request, image_id, tag_group_id, tag_id, gene_link_id):
        '''
            Method for getting multiple GeneLinks either through search
            or general listing.
        '''
        params = dict((key, val) for key, val in request.QUERY_PARAMS.iteritems())
        params['tag_id'] = tag_id
        params['image_id'] = image_id
        params['tag_group_id'] = tag_group_id
        params['gene_link_id'] = gene_link_id
        form = SingleGetForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))

    def delete(self, request, image_id, tag_group_id, tag_id, gene_link_id):
        '''
            Method for deleting a GeneLink.
        '''
        params = dict((key, val) for key, val in request.QUERY_PARAMS.iteritems())
        params['tag_id'] = tag_id
        params['image_id'] = image_id
        params['tag_group_id'] = tag_group_id
        params['gene_link_id'] = gene_link_id
        form = DeleteForm(params)

        if not form.is_valid():
            raise BadRequestException()

        return Response(form.submit(request))
