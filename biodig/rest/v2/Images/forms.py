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
from biodig.base.imageengine.exceptions import MissingFile

def load_class(full_class_string):
    """
    dynamically load a class from a string
    """

    class_data = full_class_string.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]

    module = importlib.import_module(module_path)
    # Finally, we retrieve the Class
    return getattr(module, class_str)

ImageEngine = load_class(settings.IMAGE_ENGINE)

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

        if not imageEngine.validate(originalFilename):
            os.remove(originalFilename)
            raise BadRequestException()

        normalizedFilename = imageEngine.normalize(originalFilename)
        thumbnailFilename = imageEngine.thumbnail(normalizedFilename)
        imageURL = imageEngine.save_image(normalizedFilename)
        thumbnailURL = imageEngine.save_thumbnail(thumbnailFilename)
        
        upload = Picture(imageName=imageURL, thumbnail=thumbnailURL, user=request.user,
            description=self.cleaned_data['description'], altText=self.cleaned_data['altText'],
            isPrivate=(not request.user.is_staff))
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

    def clean_image_id(self):
        '''
            Cleans the data for this form to normalize parameters.
        '''
        if self.cleaned_data['image_id'] < 0: raise ValidationError("The given image id is incorrect.")
        return self.cleaned_data['image_id']
    
    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for deleting a Image
            once the form has cleaned the input data.
        '''
        try:
            image = Picture.objects.get(pk__exact=self.cleaned_data['image_id'])
            if not request.user.is_staff and image.isPrivate and image.user != request.user:
                raise PermissionDenied()
        except Picture.DoesNotExist:
            raise ImageDoesNotExist()

        imageEngine = ImageEngine()

        try:
            image.delete()
            try:
                imageEngine.delete_image(image.imageName)
            except MissingFile:
                # a MissingFile error here means it cannot find the file to delete
                # which is not a problem since we were deleting it anyway
                pass
            try:
                imageEngine.delete_thumbnail(image.thumbnail)
            except MissingFile:
                # a MissingFile error here means it cannot find the file to delete
                # which is not a problem since we were deleting it anyway
                pass
        except DatabaseError:
            transaction.rollback()
            raise DatabaseIntegrity()

        return ImageSerializer(image).data


class PutForm(forms.Form):
    # Path Parameters
    image_id = forms.IntegerField(required=True)

    # Data Body Parameters
    description = forms.CharField(required=False)
    altText = forms.CharField(required=False)

    def clean(self):
        '''
            Cleans the data for this form to normalize parameters.
        '''
        if self.cleaned_data['image_id'] < 0: raise ValidationError("The given image id is incorrect.")
        return self.cleaned_data

    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for updating a Image
            once the form has cleaned the input data.
        '''
        image = Picture.objects.get(pk__exact=self.cleaned_data['image_id'])
        if not request.user.is_staff and image.isPrivate and image.user != request.user:
            raise PermissionDenied()

        if self.cleaned_data['description']:
            image.description = description
        if self.cleaned_data['altText']:
            image.altText = altText

        try:
            image.save()
        except DatabaseError:
            transaction.rollback()
            raise DatabaseIntegrity()

        return ImageSerializer(image).data 

class SingleGetForm(forms.Form):
    # Path Parameters
    image_id = forms.IntegerField(required=True)

    def clean_image_id(self):
        '''
            Cleans the data for this form to normalize parameters.
        '''
        if self.cleaned_data['image_id'] < 0: raise ValidationError("The given image id is incorrect.")
        return self.cleaned_data['image_id']

    def submit(self, request):
        '''
            Submits the form for getting a Image
            once the form has cleaned the input data.
        '''
        try:
            image = Picture.objects.get(pk__exact=self.cleaned_data['image_id'])
            # check permissions
            if not request.user.is_staff and image.isPrivate and image.user != request.user:
                raise PermissionDenied()
        except Picture.DoesNotExist:
            raise ImageDoesNotExist()

        return ImageSerializer(image).data
