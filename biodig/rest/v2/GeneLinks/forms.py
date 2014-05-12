'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for GeneLinks.

    Created on April 9, 2014

    @author: Andrew Oberlin
'''
from django import forms
from biodig.base.models import Image, TagGroup, Tag, GeneLink, Feature
from biodig.base import forms as bioforms
from biodig.base.serializers import GeneLinkSerializer, FeatureSerializer
from biodig.base.exceptions import OrganismDoesNotExist, ImageDoesNotExist, GeneLinkDoesNotExist, TagDoesNotExist, DatabaseIntegrity, TagGroupDoesNotExist
from rest_framework.exceptions import PermissionDenied
from django.db import transaction, DatabaseError
from django.core.exceptions import ValidationError
import numbers

class FormUtil:
    @staticmethod
    def clean_organism_id(data):
        '''
            Checks that the organism_id is a positive number..
        '''
        if data['organism_id'] < 0: raise ValidationError("The given organism id is incorrect.")
        return data['organism_id']

    @staticmethod
    def clean_feature_id(data):
        '''
            Checks that the feature_id is a positive number..
        '''
        if data['feature_id'] < 0: raise ValidationError("The given feature id is incorrect.")
        return data['feature_id']

    @staticmethod
    def clean_image_id(data):
        '''
            Checks that the image_id is a positive integer.
        '''
        if data['image_id'] < 0: raise ValidationError("The given image id is incorrect.")
        return data['image_id']

    @staticmethod
    def clean_tag_group_id(data):
        '''
            Checks that the tag_group_id is a positive number..
        '''
        if data['tag_group_id'] < 0: raise ValidationError("The given tag group id is incorrect.")
        return data['tag_group_id']

    @staticmethod
    def clean_tag_id(data):
        '''
            Checks that the tag_id is a positive number..
        '''
        if data['tag_id'] < 0: raise ValidationError("The given tag id is incorrect.")
        return data['tag_id']

    @staticmethod
    def clean_gene_link_id(data):
        '''
            Checks that the gene_link_id is a positive number..
        '''
        if data['gene_link_id'] < 0: raise ValidationError("The given gene link id is incorrect.")
        return data['gene_link_id']

    @staticmethod
    def check_permissions(table, user, readonly=True):
        if readonly:
            if table.isPrivate:
                if user and user.is_authenticated():
                    if not user.is_staff and table.user != user:
                        raise PermissionDenied()
                else:
                    raise PermissionDenied()
        else: # on POST, PUT, DELETE the user must exist and be authenticated automatically
            if not user.is_staff and table.user != user: # only staff and owners can edit
                raise PermissionDenied()

    @staticmethod
    def get_containers(image_id, tag_group_id, tag_id, user, readonly=True):
        try:
            image = Image.objects.get(pk__exact=image_id)
            FormUtil.check_permissions(image, user, readonly=readonly)
        except Image.DoesNotExist:
            raise ImageDoesNotExist()

        try:
            group = TagGroup.objects.get(pk__exact=tag_group_id, picture=image)
            FormUtil.check_permissions(group, user, readonly=readonly)
        except TagGroup.DoesNotExist:
            raise TagGroupDoesNotExist()

        try:
            tag = Tag.objects.get(pk__exact=tag_id, group=group)
            FormUtil.check_permissions(tag, user, readonly=readonly)
        except Tag.DoesNotExist:
            raise TagDoesNotExist()

        return image, group, tag


class MultiGetForm(forms.Form):
    # Query Parameters
    offset = forms.IntegerField(required=False)
    limit = forms.IntegerField(required=False)
    # Gene Link filters
    lastModified = bioforms.DateTimeRangeField(required=False)
    dateCreated = bioforms.DateTimeRangeField(required=False)
    owner = forms.IntegerField(required=False)

    # Path Parameters
    image_id = forms.IntegerField(required=True)
    tag_group_id = forms.IntegerField(required=True)
    tag_id = forms.IntegerField(required=True)

    def clean_image_id(self):
        return FormUtil.clean_image_id(self.cleaned_data)

    def clean_tag_group_id(self):
        return FormUtil.clean_tag_group_id(self.cleaned_data)

    def clean_tag_id(self):
        return FormUtil.clean_tag_id(self.cleaned_data)

    def clean(self):
        if not self.cleaned_data['offset']: self.cleaned_data['offset'] = 0
        return self.cleaned_data


    def submit(self, request):
        '''
            Submits the form for getting multiple GeneLinks
            once the form has cleaned the input data.
        '''
        qbuild = bioforms.QueryBuilder(GeneLink)

        # find the tag group that contains the tag
        image, group, tag = FormUtil.get_containers(self.cleaned_data['image_id'], self.cleaned_data['tag_group_id'],
            self.cleaned_data['tag_id'], request.user)

        # add permissions to query
        if request.user and request.user.is_authenticated():
            if not request.user.is_staff:
                qbuild.q = qbuild().filter(isPrivate=False) | GeneLink.objects.filter(user__pk__exact=request.user.pk)
        else:
            qbuild.q = qbuild().filter(isPrivate=False)

        filterkeys = ['lastModified', 'dateCreated']
        for key in filterkeys:
            qbuild.filter(key, self.cleaned_data[key])

        qbuild.filter('user', self.cleaned_data['owner'])

        if not self.cleaned_data['limit'] or self.cleaned_data['limit'] < 0:
            qbuild.q = qbuild()[self.cleaned_data['offset']:]
        else:
            qbuild.q = qbuild()[self.cleaned_data['offset'] : self.cleaned_data['offset']+self.cleaned_data['limit']]

        return GeneLinkSerializer(qbuild(), many=True).data

class PostForm(forms.Form):
    # Path Parameters
    image_id = forms.IntegerField(required=True)
    tag_group_id = forms.IntegerField(required=True)
    tag_id = forms.IntegerField(required=True)

    # POST body data
    feature_id = forms.IntegerField(required=True)
    organism_id = forms.IntegerField(required=True)

    def clean_organism_id(self):
        return FormUtil.clean_organism_id(self.cleaned_data)

    def clean_feature_id(self):
        return FormUtil.clean_feature_id(self.cleaned_data)

    def clean_image_id(self):
        return FormUtil.clean_image_id(self.cleaned_data)

    def clean_tag_group_id(self):
        return FormUtil.clean_tag_group_id(self.cleaned_data)

    def clean_tag_id(self):
        return FormUtil.clean_points(self.cleaned_data)

    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for creating a GeneLink
            once the form has cleaned the input data.
        '''
        image, group, tag = FormUtil.get_containers(self.cleaned_data['image_id'], self.cleaned_data['tag_group_id'],
            self.cleaned_data['tag_id'], request.user, readonly=False)

        try:
            organism = Organism.objects.get(pk__exact=self.cleaned_data['organism_id'])
        except Organism.DoesNotExist:
            raise OrganismDoesNotExist()

        try:
            feature = Feature.objects.get(pk__exact=self.cleaned_data['feature_id'], organism__exact=organism)
        except Feature.DoesNotExist:
            raise FeatureDoesNotExist()

        geneLink = GeneLink(tag=tag, feature=feature, user=request.user)

        try:
            geneLink.save()
            tag.save()
            group.save()
            image.save()
        except DatabaseError:
            transaction.rollback()
            raise DatabaseIntegrity()

        return GeneLinkSerializer(geneLink).data


class DeleteForm(forms.Form):
    # Path paramaters
    image_id = forms.IntegerField(required=True)
    tag_group_id = forms.IntegerField(required=True)
    tag_id = forms.IntegerField(required=True)
    gene_link_id = forms.IntegerField(required=True)

    def clean_gene_link_id(self):
        return FormCleaningUtil.clean_gene_link_id(self.cleaned_data)

    def clean_tag_id(self):
        return FormCleaningUtil.clean_tag_id(self.cleaned_data)

    def clean_tag_group_id(self):
        return FormCleaningUtil.clean_tag_group_id(self.cleaned_data)

    def clean_image_id(self):
        return FormCleaningUtil.clean_image_id(self.cleaned_data)

    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for deleting a GeneLink
            once the form has cleaned the input data.
        '''
        image, group, tag = FormUtil.get_containers(self.cleaned_data['image_id'], self.cleaned_data['tag_group_id'],
            self.cleaned_data['tag_id'], request.user, readonly=False)

        try:
            geneLink = GeneLink.objects.get(tag=tag, pk__exact=self.cleaned_data['gene_link_id'])
        except GeneLink.DoesNotExist:
            raise GeneLinkDoesNotExist()

        serialized = GeneLinkSerializer(geneLink).data

        try:
            geneLink.delete()
            tag.save()
            group.save()
            image.save()
        except DatabaseError:
            transaction.rollback()
            raise DatabaseIntegrity()

        return serialized

class SingleGetForm(forms.Form):
    # Path parameters
    image_id = forms.IntegerField(required=True)
    tag_group_id = forms.IntegerField(required=True)
    tag_id = forms.IntegerField(required=True)
    gene_link_id = forms.IntegerField(required=True)

    def clean_gene_link_id(self):
        return FormCleaningUtil.clean_gene_link_id(self.cleaned_data)

    def clean_tag_id(self):
        return FormCleaningUtil.clean_tag_id(self.cleaned_data)

    def clean_tag_group_id(self):
        return FormCleaningUtil.clean_tag_group_id(self.cleaned_data)

    def clean_image_id(self):
        return FormCleaningUtil.clean_image_id(self.cleaned_data)

    def submit(self, request):
        '''
            Submits the form for getting a GeneLink
            once the form has cleaned the input data.
        '''
        image, group, tag = FormUtil.get_containers(self.cleaned_data['image_id'], self.cleaned_data['tag_group_id'],
            self.cleaned_data['tag_id'], request.user)
        try:
            geneLink = GeneLink.objects.get(tag=tag, pk__exact=self.cleaned_data['gene_link_id'])
        except GeneLink.DoesNotExist:
            raise GeneLinkDoesNotExist()

        return GeneLinkSerializer(geneLink).data
