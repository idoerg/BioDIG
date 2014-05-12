'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for PublicationRequests.

    Created on May 12, 2014

    @author: Andrew Oberlin
'''
from django import forms
from biodig.base.models import PublicationRequest, Image, TagGroup, Tag, GeneLink
from biodig.base import forms as bioforms
from biodig.base.serializers import PublicationRequestSerializer, PublicationRequestPreviewSerializer
from biodig.base.exceptions import PublicationRequestDoesNotExist, ImageDoesNotExist, DatabaseIntegrity
from rest_framework.exceptions import PermissionDenied
from django.db import transaction, DatabaseError
from django.core.exceptions import ValidationError
import datetime

class FormUtil:
    @staticmethod
    def clean_publication_request_id(data):
        '''
            Cleans an publication_request id ensuring that it is a positive integer.
        '''
        if data['publication_request_id'] < 0:
            raise ValidationError("PublicationRequest id is incorrect.")
        return data['publication_request_id']

    @staticmethod
    def clean_image_id(data):
        '''
            Cleans an image id ensuring that it is a positive integer.
        '''
        if data['image_id'] < 0:
            raise ValidationError("Image id is incorrect.")
        return data['image_id']

class MultiGetForm(forms.Form):
    # Query Parameters
    offset = forms.IntegerField(required=False)
    limit = forms.IntegerField(required=False)

    def clean_publication_request_id(self):
        return FormUtil.clean_publication_request_id(self.cleaned_data)

    def clean(self):
        if not self.cleaned_data['offset']: self.cleaned_data['offset'] = 0
        return self.cleaned_data

    def submit(self, request):
        '''
            Submits the form for getting multiple PublicationRequests
            once the form has cleaned the input data.
        '''
        qbuild = bioforms.QueryBuilder(PublicationRequest)
        if not request.user.is_staff:
            qbuild.filter('user', request.user)

        if not self.cleaned_data['limit'] or self.cleaned_data['limit'] < 0:
            qbuild.q = qbuild()[self.cleaned_data['offset']:]
        else:
            qbuild.q = qbuild()[self.cleaned_data['offset'] : self.cleaned_data['offset']+self.cleaned_data['limit']]

        return PublicationRequestSerializer(qbuild(), many=True).data

class PostForm(forms.Form):
    # Data Body Parameters
    image_id = forms.IntegerField(required=True)
    preview = forms.BooleanField(required=False)

    def clean_image_id(self):
        return FormUtil.clean_image_id(self.cleaned_data)

    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for creating a PublicationRequest
            once the form has cleaned the input data.
        '''
        try:
            image = Image.objects.get(pk__exact=self.cleaned_data['image_id'])
        except Image.DoesNotExist:
            raise ImageDoesNotExist()

        # check to see if the user has permissions to publish changes on this image
        permitted = not image.isPrivate or image.user == request.user or request.user.is_staff
        if not permitted:
            raise PermissionDenied()

        pubrequest = PublicationRequest(target=image, user=request.user)


        if not self.cleaned_data['preview']:
            try:
                pubrequest.save()
            except DatabaseError:
                transaction.rollback()
                raise DatabaseIntegrity()

            return PublicationRequestSerializer(pubrequest).data
        else:
            # get the image that has been targeted and make it public
            image.isPrivate = False

            now = datetime.datetime.now()
            # get all the tag groups that are private and were created before the timestamp
            # on the request and were on the image targeted and were created by the request's user
            tagGroups = TagGroup.objects.filter(picture=image, isPrivate=True, user=pubrequest.user,
                dateCreated__lt=now)

            # get all the tags that are private and were created before the timestamp on the
            # request and were in one of the tag groups being updated and were created by the
            # request's user
            tags = Tag.objects.filter(group__in=tagGroups, isPrivate=True, user=pubrequest.user,
                dateCreated__lt=now)

            # get all the gene links that are private and were created before the timestamp on the
            # request and were in one of the tags being updated and were created by the
            # request's user
            geneLinks = GeneLink.objects.filter(tag__in=tags, isPrivate=True, user=pubrequest.user,
                dateCreated__lt=now)

            for tagGroup in tagGroups:
                tagGroup.isPrivate = False

            for tag in tags:
                tag.isPrivate = False

            for geneLink in geneLinks:
                geneLink.isPrivate = False

            return PublicationRequestPreviewSerializer(image, tagGroups, tags, geneLinks).data

class PutForm(forms.Form):
    # Path Parameters
    publication_request_id = forms.IntegerField(required=True)

    def clean_publication_request_id(self):
        return FormUtil.clean_publication_request_id(self.cleaned_data)


    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for fulfilling a PublicationRequest
            once the form has cleaned the input data.
        '''
        try:
            pubrequest = PublicationRequest.objects.get(pk__exact=self.cleaned_data['publication_request_id'])
        except PublicationRequest.DoesNotExist:
            raise PublicationRequestDoesNotExist()

        if not request.user.is_staff:
            raise PermissionDenied()

        # update the pubrequest to show that it is running
        try:
            pubrequest.status = PublicationRequest.RUNNING
            pubrequest.save()
        except DatabaseError:
            transaction.rollback()
            raise DatabaseIntegrity()

        # get the image that has been targeted and make it public
        try:
            image = Image.objects.get(pk__exact=pubrequest.target)
            image.isPrivate = False
        except Image.DoesNotExist:
            raise ImageDoesNotExist()

        # get all the tag groups that are private and were created before the timestamp
        # on the request and were on the image targeted and were created by the request's user
        tagGroups = TagGroup.objects.filter(image=image, isPrivate=True, user=pubrequest.user,
            dateCreated__lt=pubrequest.dateCreated)

        # get all the tags that are private and were created before the timestamp on the
        # request and were in one of the tag groups being updated and were created by the
        # request's user
        tags = Tag.objects.filter(group__in=tagGroups, isPrivate=True, user=pubrequest.user,
            dateCreated__lt=pubrequest.dateCreated)

        # get all the gene links that are private and were created before the timestamp on the
        # request and were in one of the tags being updated and were created by the
        # request's user
        geneLinks = GeneLink.objects.filter(tag__in=tags, isPrivate=True, user=pubrequest.user,
            dateCreated__lt=pubrequest.dateCreated)

        serialized = PublicationRequestSerializer(pubrequest).data

        # save all the changes
        try:
            image.save()
            tagGroups.update(isPrivate=False)
            tags.update(isPrivate=False)
            geneLinks.update(isPrivate=False)
            pubrequest.delete()
        except DatabaseError:
            transaction.rollback()
            raise DatabaseIntegrity()

        return serialized


class DeleteForm(forms.Form):
    # Path Parameters
    publication_request_id = forms.IntegerField(required=True)

    def clean_publication_request_id(self):
        return FormUtil.clean_publication_request_id(self.cleaned_data)

    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for deleting a PublicationRequest
            once the form has cleaned the input data.
        '''
        try:
            pubrequest = PublicationRequest.objects.get(pk__exact=self.cleaned_data['publication_request_id'])
        except PublicationRequest.DoesNotExist:
            raise PublicationRequestDoesNotExist()

        if pubrequest.user != request.user and not request.user.is_staff:
            raise PermissionDenied()

        serialized = PublicationRequestSerializer(pubrequest).data

        try:
            pubrequest.delete()
        except DatabaseError:
            transaction.rollback()
            raise DatabaseIntegrity()

        return serialized

class SingleGetForm(forms.Form):
    # Path Parameters
    publication_request_id = forms.IntegerField(required=True)

    def clean_publication_request_id(self):
        return FormUtil.clean_publication_request_id(self.cleaned_data)

    def submit(self, request):
        '''
            Submits the form for getting an PublicationRequest
            once the form has cleaned the input data.
        '''
        try:
            pubrequest = PublicationRequest.objects.get(pk__exact=self.cleaned_data['publication_request_id'])
        except PublicationRequest.DoesNotExist:
            raise PublicationRequestDoesNotExist()

        if pubrequest.user != request.user and not request.user.is_staff:
            raise PermissionDenied()

        return PublicationRequestSerializer(pubrequest).data

class PreviewForm(forms.Form):
    # Path Parameters
    publication_request_id = forms.IntegerField(required=True)

    def clean_publication_request_id(self):
        return FormUtil.clean_publication_request_id(self.cleaned_data)

    def submit(self, request):
        '''
            Submits the form for getting an PublicationRequest's preview
            once the form has cleaned the input data.
        '''
        try:
            pubrequest = PublicationRequest.objects.get(pk__exact=self.cleaned_data['publication_request_id'])
        except PublicationRequest.DoesNotExist:
            raise PublicationRequestDoesNotExist()

        if pubrequest.user != request.user and not request.user.is_staff:
            raise PermissionDenied()

        # get the image that has been targeted and make it public
        try:
            image = Image.objects.get(pk__exact=pubrequest.target)
            image.isPrivate = False
        except Image.DoesNotExist:
            raise ImageDoesNotExist()

        # get all the tag groups that are private and were created before the timestamp
        # on the request and were on the image targeted and were created by the request's user
        tagGroups = TagGroup.objects.filter(image=image, isPrivate=True, user=pubrequest.user,
            dateCreated__lt=pubrequest.dateCreated)

        # get all the tags that are private and were created before the timestamp on the
        # request and were in one of the tag groups being updated and were created by the
        # request's user
        tags = Tag.objects.filter(group__in=tagGroups, isPrivate=True, user=pubrequest.user,
            dateCreated__lt=pubrequest.dateCreated)

        # get all the gene links that are private and were created before the timestamp on the
        # request and were in one of the tags being updated and were created by the
        # request's user
        geneLinks = GeneLink.objects.filter(tag__in=tags, isPrivate=True, user=pubrequest.user,
            dateCreated__lt=pubrequest.dateCreated)

        return PublicationRequestPreviewSerializer(image, tagGroups, tags, geneLinks).data
