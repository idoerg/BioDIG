'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for Tags.
    
    Created on February 10, 2013

    @author: Andrew Oberlin
'''
from django import forms
from biodig.base.models import Tag, TagGroup, Picture
from biodig.base import forms as bioforms
from biodig.base.serializers import TagSerializer
from biodig.base.exceptions import ImageDoesNotExist, DatabaseIntegrity, TagGroupDoesNotExist
from rest_framework.exceptions import PermissionDenied
from django.db import transaction, DatabaseError
from django.core.exceptions import ValidationError

class MultiGetForm(forms.Form):
    # Query Parameters
    offset = forms.IntegerField(required=False)
    limit = forms.IntegerField(required=False)
    # Tag filters
    lastModified = bioforms.DateTimeRangeField(required=False)
    dateCreated = bioforms.DateTimeRangeField(required=False)
    user = forms.IntegerField(required=False)
    name = forms.CharField(required=False)
    
    # Path Parameters
    image_id = forms.IntegerField(required=True)
    tag_group_id = forms.IntegerField(required=True)

    def clean(self):
        if not self.cleaned_data['offset']: self.cleaned_data['offset'] = 0
        return self.cleaned_data


    def submit(self, request):
        '''
            Submits the form for getting multiple Tags
            once the form has cleaned the input data.
        '''
        qbuild = bioforms.QueryBuilder(Tag)
        
        # find the tag group that contains the tag
        try:
            group = TagGroup.objects.get(pk__exact=self.cleaned_data['tag_group_id'], picture__exact=self.cleaned_data['image_id'])
            
            # check tag group permissions
            if not group.readPermissions(request.user):
                raise PermissionDenied()
            
            qbuild.filter('group', group, match='')
        except (TagGroup.DoesNotExist, ValueError):
            raise TagGroupDoesNotExist()
        
        # add permissions to query
        if request.user and request.user.is_authenticated():
            if not request.user.is_staff:
                qbuild.q = qbuild().filter(isPrivate = False) | Tag.objects.filter(user__pk__exact=request.user.pk)
        else:
            qbuild.q = qbuild().filter(isPrivate=False)
        
        filterkeys = ['name', 'user', 'lastModified', 'dateCreated']
        for key in filterkeys:
            qbuild.filter(key, self.cleaned_data[key])
            
        if not self.cleaned_data['limit'] or self.cleaned_data['limit'] < 0:
            qbuild.q = qbuild()[self.cleaned_data['offset']:]
        else:
            qbuild.q = qbuild()[self.cleaned_data['offset'] : self.cleaned_data['offset']+self.cleaned_data['limit']]

        return TagSerializer(qbuild(), many=True).data

class PostForm(forms.Form):
    image_id = forms.IntegerField(required=True)
    tag_group_id = forms.IntegerField(required=True)
    name = forms.CharField(required=True)
    points = bioforms.JsonField(required=True)
    color = bioforms.JsonField(required=True)

    def clean(self):
        '''
            Cleans the data and checks to see if the image id is
            a valid input.
        '''
        if self.cleaned_data['image_id'] < 0: raise ValidationError("The given image id is incorrect.")
        if self.cleaned_data['tag_group_id'] < 0: raise ValidationError("The given tag group id is incorrect.")
        return self.cleaned_data
    
    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for creating a Tag
            once the form has cleaned the input data.
        '''
        try:
            group = TagGroup.objects.get(pk__exact=self.cleaned_data['tag_group_id'], picture__exact=self.cleaned_data['image_id'])
            
            # check tag group permissions
            if not group.writePermissions(request.user):
                raise PermissionDenied()
        except (TagGroup.DoesNotExist, ValueError):
            raise TagGroupDoesNotExist()
        
        # start saving the new tag now that it has passed all tests
        tag = Tag()
        try:
            tag.save()
        except DatabaseError:
            transaction.rollback()
            raise DatabaseIntegrity()

        return TagSerializer(tag).data

class DeleteForm(forms.Form):
    tag_group_id = forms.IntegerField(required=True)

    def clean(self):
        '''
            Cleans the data for this form to normalize parameters.
        '''
        if self.cleaned_data['tag_group_id'] < 0: raise ValidationError("The given tag group id is incorrect.")
        return self.cleaned_data
    
    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for deleting a TagGroup
            once the form has cleaned the input data.
        '''
        
        try:
            group = TagGroup.objects.get(pk__exact=self.cleaned_data['tag_group_id'])
        except (TagGroup.DoesNotExist, ValueError):
            raise TagGroupDoesNotExist()
        
        if not group.writePermissions(request.user):
            raise PermissionDenied()
       
        serialized = TagSerializer(group).data

        try:
            group.delete()
        except DatabaseError:
            transaction.rollback()
            raise DatabaseIntegrity()
        
        return serialized

class PutForm(forms.Form):
    tag_group_id = forms.IntegerField(required=True)

    def clean(self):
        '''
            Cleans the data for this form to normalize parameters.
        '''
        if self.cleaned_data['tag_group_id'] < 0: raise ValidationError("The given tag group id is incorrect.")
        return self.cleaned_data

    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for updating a Tag
            once the form has cleaned the input data.
        '''
        try:
            group = TagGroup.objects.get(pk__exact=self.cleaned_data['tag_group_id'])
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

        return TagSerializer(group).data

class SingleGetForm(forms.Form):
    tag_group_id = forms.IntegerField(required=True)

    def clean(self):
        '''
            Cleans the data for this form to normalize parameters.
        '''
        if self.cleaned_data['tag_group_id'] < 0: raise ValidationError("The given tag group id is incorrect.")
        return self.cleaned_data

    def submit(self, request):
        '''
            Submits the form for getting a Tag
            once the form has cleaned the input data.
        '''
        try:
            group = TagGroup.objects.get(pk__exact=self.cleaned_data['tag_group_id'])
        except (TagGroup.DoesNotExist, ValueError):
            raise TagGroupDoesNotExist()

        if not group.readPermissions(request.user):
            raise PermissionDenied()

        return TagSerializer(group).data
