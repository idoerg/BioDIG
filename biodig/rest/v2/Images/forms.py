'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for Images.
    
    Created on March 5, 2013

    @author: Andrew Oberlin
'''
from django import forms
from biodig.base.models import Picture
from biodig.base import forms as bioforms
from biodig.base.serializers import ImageSerializer
from biodig.base.exceptions import ImageDoesNotExist, DatabaseIntegrity,\
    BadRequestException, NotImplementedException
from rest_framework.exceptions import PermissionDenied
from django.db import transaction, DatabaseError
from django.core.exceptions import ValidationError
import importlib
from django.conf import settings
import time
import os
ImageEngine = importlib.import_module(settings.IMAGE_ENGINE)

class MultiGetForm(forms.Form):
    # Query Parameters
    offset = forms.IntegerField(required=False)
    limit = forms.IntegerField(required=False)
    # Image filters (Query)
    dateCreated = bioforms.DateTimeRangeField(required=False)
    owner = forms.IntegerField(required=False)

    def clean(self):
        if not self.cleaned_data['offset']: self.cleaned_data['offset'] = 0
        return self.cleaned_data


    def submit(self, request):
        '''
            Submits the form for getting multiple TagGroups
            once the form has cleaned the input data.
        '''
        qbuild = bioforms.QueryBuilder(Picture)
        
        # add permissions to query
        if request.user and request.user.is_authenticated():
            if not request.user.is_staff:
                qbuild.q = qbuild().filter(isPrivate = False) | Picture.objects.filter(user__pk__exact=request.user.pk)
        else:
            qbuild.q = qbuild().filter(isPrivate=False)
        
        filterkeys = {
            'user' : 'owner',
            'uploadDate' : 'dateCreated'
        }
        for buildkey, key in filterkeys.iteritems():
            qbuild.filter(buildkey, self.cleaned_data[key])
            
        if not self.cleaned_data['limit'] or self.cleaned_data['limit'] < 0:
            qbuild.q = qbuild()[self.cleaned_data['offset']:]
        else:
            qbuild.q = qbuild()[self.cleaned_data['offset'] : self.cleaned_data['offset']+self.cleaned_data['limit']]

        return ImageSerializer(qbuild(), many=True).data

class PostForm(forms.Form):
    # POST (data section) Body Parameters
    description = forms.CharField(required=True)
    altText = forms.CharField(required=True)
    image = forms.FileField(required=True)
    
    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for creating a Image
            once the form has cleaned the input data.
        '''
        imageEngine = ImageEngine()
        image = self.cleaned_data['image']
        if imageEngine.validate(image):
            raise BadRequestException()

        now = str(time.time())
        originalFilename = os.path.join(
            os.path.join(
                settings.MEDIA_ROOT, os.path.join('cache', 'pictures')
            ), 
            now + image.name
        )
    
        # writes the chunks in the file upload to the cache file
        with open(originalFilename, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        normalizedFilename = imageEngine.normalize(originalFilename)
        thumbnailFilename = imageEngine.thumbnail(normalizedFilename)
        imageURL = imageEngine.saveImage(normalizedFilename)
        thumbnailURL = imageEngine.saveThumbnail(thumbnailFilename)
        
        upload = Picture(imageName=imageURL, thumbnail=thumbnailURL, user=self.user, isPrivate=(not request.user.is_staff))
        try:
            upload.save()
        except DatabaseError:
            transaction.rollback()
            os.remove(normalizedFilename)
            os.remove(thumbnailFilename)
            raise DatabaseIntegrity()

        return ImageSerializer(upload).data

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
            Submits the form for deleting a Image
            once the form has cleaned the input data.
        '''
        raise NotImplementedException()

class PutForm(forms.Form):
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
            Submits the form for updating a Image
            once the form has cleaned the input data.
        '''
        raise NotImplementedException()

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
            Submits the form for getting a Image
            once the form has cleaned the input data.
        '''
        raise NotImplementedException()
