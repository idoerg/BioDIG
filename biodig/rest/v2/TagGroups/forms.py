'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for Tag Groups.

    Created on January 13, 2013

    @author: Andrew Oberlin
'''
from django import forms
from biodig.base.models import TagGroup, Image
from biodig.base import forms as bioforms
from biodig.base.serializers import TagGroupSerializer
from biodig.base.exceptions import ImageDoesNotExist, DatabaseIntegrity, TagGroupDoesNotExist
from rest_framework.exceptions import PermissionDenied
from django.db import transaction, DatabaseError
from django.core.exceptions import ValidationError

class MultiGetForm(forms.Form):
    # Query Parameters
    offset = forms.IntegerField(required=False)
    limit = forms.IntegerField(required=False)
    # Tag Group filters (Query)
    lastModified = bioforms.DateTimeRangeField(required=False)
    dateCreated = bioforms.DateTimeRangeField(required=False)
    owner = forms.IntegerField(required=False)
    name = forms.CharField(required=False)

    # Path Parameters
    image_id = forms.IntegerField(required=True)

    def clean(self):
        if not self.cleaned_data['offset']: self.cleaned_data['offset'] = 0
        return self.cleaned_data


    def submit(self, request):
        '''
            Submits the form for getting multiple TagGroups
            once the form has cleaned the input data.
        '''
        qbuild = bioforms.QueryBuilder(TagGroup)

        # add permissions to query
        if request.user and request.user.is_authenticated():
            if not request.user.is_staff:
                qbuild.q = qbuild().filter(isPrivate = False) | TagGroup.objects.filter(user__pk__exact=request.user.pk)
        else:
            qbuild.q = qbuild().filter(isPrivate=False)

        filterkeys = {
            'name' : 'name', 'user' : 'owner',
            'lastModified' : 'lastModified',
            'dateCreated' : 'dateCreated',
            'picture' : 'image_id'
        }
        for buildkey, key in filterkeys.iteritems():
            qbuild.filter(buildkey, self.cleaned_data[key])

        if not self.cleaned_data['limit'] or self.cleaned_data['limit'] < 0:
            qbuild.q = qbuild()[self.cleaned_data['offset']:]
        else:
            qbuild.q = qbuild()[self.cleaned_data['offset'] : self.cleaned_data['offset']+self.cleaned_data['limit']]

        return TagGroupSerializer(qbuild(), many=True).data

class PostForm(forms.Form):
    # Path Parameters
    image_id = forms.IntegerField(required=True)

    # POST (data section) Body Parameters
    name = forms.CharField(required=True)

    def clean(self):
        '''
            Cleans the data and checks to see if the image id is
            a valid input.
        '''
        if self.cleaned_data['image_id'] < 0: raise ValidationError("The given image id is incorrect.")
        return self.cleaned_data

    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for creating a TagGroup
            once the form has cleaned the input data.
        '''
        try:
            image = Image.objects.get(pk__exact=self.cleaned_data['image_id'])
        except (Image.DoesNotExist, ValueError):
            raise ImageDoesNotExist()

        if not image.writePermissions(request.user):
            raise PermissionDenied()

        # start saving the new tag now that it has passed all tests
        tagGroup = TagGroup(name=self.cleaned_data['name'], picture=image, user=request.user)
        try:
            tagGroup.save()
        except DatabaseError:
            transaction.rollback()
            raise DatabaseIntegrity()

        return TagGroupSerializer(tagGroup).data

class DeleteForm(forms.Form):
    # Path Parameters
    image_id = forms.IntegerField(required=True)
    tag_group_id = forms.IntegerField(required=True)

    def clean(self):
        '''
            Cleans the data for this form to normalize parameters.
        '''
        if self.cleaned_data['image_id'] < 0: raise ValidationError("The given image id is incorrect.")
        if self.cleaned_data['tag_group_id'] < 0: raise ValidationError("The given tag group id is incorrect.")
        return self.cleaned_data

    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for deleting a TagGroup
            once the form has cleaned the input data.
        '''

        try:
            group = TagGroup.objects.get(pk__exact=self.cleaned_data['tag_group_id'], picture__exact=self.cleaned_data['image_id'])
        except (TagGroup.DoesNotExist, ValueError):
            raise TagGroupDoesNotExist()

        if not group.writePermissions(request.user):
            raise PermissionDenied()

        serialized = TagGroupSerializer(group).data

        try:
            group.delete()
        except DatabaseError:
            transaction.rollback()
            raise DatabaseIntegrity()

        return serialized

class PutForm(forms.Form):
    # Path Parameters
    image_id = forms.IntegerField(required=True)
    tag_group_id = forms.IntegerField(required=True)

    # Data Body Parameters
    name = forms.CharField(required=True)

    def clean(self):
        '''
            Cleans the data for this form to normalize parameters.
        '''
        if self.cleaned_data['image_id'] < 0: raise ValidationError("The given image id is incorrect.")
        if self.cleaned_data['tag_group_id'] < 0: raise ValidationError("The given tag group id is incorrect.")
        return self.cleaned_data

    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for updating a TagGroup
            once the form has cleaned the input data.
        '''
        try:
            group = TagGroup.objects.get(pk__exact=self.cleaned_data['tag_group_id'], picture__exact=self.cleaned_data['image_id'])
        except (TagGroup.DoesNotExist, ValueError):
            raise TagGroupDoesNotExist()

        if not group.writePermissions(request.user):
            raise PermissionDenied()

        # update the name
        if self.cleaned_data['name']:
            group.name = self.cleaned_data['name']

        try:
            group.save()
        except DatabaseError:
            transaction.rollback()
            raise DatabaseIntegrity()

        return TagGroupSerializer(group).data

class SingleGetForm(forms.Form):
    # Path Parameters
    image_id = forms.IntegerField(required=True)
    tag_group_id = forms.IntegerField(required=True)

    def clean(self):
        '''
            Cleans the data for this form to normalize parameters.
        '''
        if self.cleaned_data['image_id'] < 0: raise ValidationError("The given image id is incorrect.")
        if self.cleaned_data['tag_group_id'] < 0: raise ValidationError("The given tag group id is incorrect.")
        return self.cleaned_data

    def submit(self, request):
        '''
            Submits the form for getting a TagGroup
            once the form has cleaned the input data.
        '''
        try:
            group = TagGroup.objects.get(pk__exact=self.cleaned_data['tag_group_id'], picture__exact=self.cleaned_data['image_id'])
        except (TagGroup.DoesNotExist, ValueError):
            raise TagGroupDoesNotExist()

        if not group.readPermissions(request.user):
            raise PermissionDenied()

        return TagGroupSerializer(group).data
