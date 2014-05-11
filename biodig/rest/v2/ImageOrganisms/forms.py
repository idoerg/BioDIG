'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for ImageOrganisms.

    Created on January 13, 2013

    @author: Andrew Oberlin
'''
from django import forms
from biodig.base.models import Image, ImageOrganism, Organism
from biodig.base import forms as bioforms
from biodig.base.serializers import ImageOrganismSerializer
from biodig.base.exceptions import ImageOrganismDoesNotExist, ImageDoesNotExist, DatabaseIntegrity
from rest_framework.exceptions import PermissionDenied
from django.db import transaction, DatabaseError
from django.core.exceptions import ValidationError

class FormCleaningUtil:
    @staticmethod
    def clean_image_id(data):
        '''
            Cleans an image id ensuring that it is a positive integer.
        '''
        if data['image_id'] < 0:
            raise ValidationError("Image id is incorrect.")
        return data['image_id']

    @staticmethod
    def clean_organism_id(data):
        '''
            Cleans an organism id ensuring that it is a positive integer.
        '''
        if data['organism_id'] < 0:
            raise ValidationError("Organism id is incorrect.")
        return data['organism_id']

class MultiGetForm(forms.Form):
    # Query Parameters
    offset = forms.IntegerField(required=False)
    limit = forms.IntegerField(required=False)

    # Path Parameters
    image_id = forms.IntegerField(required=True)

    def clean_image_id(self):
        return FormCleaningUtil.clean_image_id(self.cleaned_data)

    def clean(self):
        if not self.cleaned_data['offset']: self.cleaned_data['offset'] = 0
        return self.cleaned_data

    def submit(self, request):
        '''
            Submits the form for getting multiple ImageOrganisms
            once the form has cleaned the input data.
        '''
        try:
            image = Image.objects.get(pk__exact=self.cleaned_data['image_id'])
        except Image.DoesNotExist:
            raise ImageDoesNotExist()

        if image.isPrivate:
            if request.user and request.user.is_authenticated():
                if not request.user.is_staff and image.user != request.user:
                    raise PermissionDenied()
            else:
                raise PermissionDenied()

        organisms = ImageOrganism.objects.filter(picture=image)

        if not self.cleaned_data['limit'] or self.cleaned_data['limit'] < 0:
            organisms = organisms[self.cleaned_data['offset']:]
        else:
            organims = organisms[self.cleaned_data['offset'] : self.cleaned_data['offset']+self.cleaned_data['limit']]

        return ImageOrganismSerializer(organisms, many=True).data

class PostForm(forms.Form):
    # Path Parameters
    image_id = forms.IntegerField(required=True)

    # POST (data section) Body Parameters
    organism_id = forms.IntegerField(required=True)

    def clean_image_id(self):
        return FormCleaningUtil.clean_image_id(self.cleaned_data)

    def clean_organism_id(self):
        return FormCleaningUtil.clean_organism_id(self.cleaned_data)

    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for creating an ImageOrganism
            once the form has cleaned the input data.
        '''
        try:
            image = Image.objects.get(pk__exact=self.cleaned_data['image_id'])
        except (Image.DoesNotExist, ValueError):
            raise ImageDoesNotExist()

        try:
            organism = Organism.objects.get(pk__exact=self.cleaned_data['organism_id'])
        except (Organism.DoesNotExist, ValueError):
            raise OrganismDoesNotExist()

        if not request.user.is_staff and image.user != request.user:
            raise PermissionDenied()

        # start saving the new tag now that it has passed all tests
        imageOrg = ImageOrganism(picture=image, organism=organism)
        try:
            imageOrg.save()
        except DatabaseError:
            transaction.rollback()
            raise DatabaseIntegrity()

        return ImageOrganismSerializer(imageOrg).data

class DeleteForm(forms.Form):
    # Path Parameters
    image_id = forms.IntegerField(required=True)
    organism_id = forms.IntegerField(required=True)

    def clean_image_id(self):
        return FormCleaningUtil.clean_image_id(self.cleaned_data)

    def clean_organism_id(self):
        return FormCleaningUtil.clean_organism_id(self.cleaned_data)

    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for deleting a ImageOrganism
            once the form has cleaned the input data.
        '''
        try:
            image = Image.objects.get(pk__exact=self.cleaned_data['image_id'])
            if not request.user.is_staff and image.user != request.user:
                raise PermissionDenied()

            imageOrg = ImageOrganism.objects.get(picture=image, organism=self.cleaned_data['organism_id'])
        except (ImageOrganism.DoesNotExist, Image.DoesNotExist):
            raise ImageOrganismDoesNotExist()

        serialized = ImageOrganismSerializer(imageOrg).data

        try:
            imageOrg.delete()
        except DatabaseError:
            transaction.rollback()
            raise DatabaseIntegrity()

        return serialized

class SingleGetForm(forms.Form):
    # Path Parameters
    image_id = forms.IntegerField(required=True)
    organism_id = forms.IntegerField(required=True)

    def clean_image_id(self):
        return FormCleaningUtil.clean_image_id(self.cleaned_data)

    def clean_organism_id(self):
        return FormCleaningUtil.clean_organism_id(self.cleaned_data)

    def submit(self, request):
        '''
            Submits the form for getting an ImageOrganism
            once the form has cleaned the input data.
        '''
        try:
            image = Image.objects.get(pk__exact=self.cleaned_data['image_id'])
        except Image.DoesNotExist:
            raise ImageDoesNotExist()

        if image.isPrivate:
            if request.user and request.user.is_authenticated():
                if not request.user.is_staff and image.user != request.user:
                    raise PermissionDenied()
            else:
                raise PermissionDenied()
        try:
            imageOrg = ImageOrganism.objects.get(picture=image, organism__exact=self.cleaned_data['organism_id'])
        except ImageOrganism.DoesNotExist:
            raise ImageOrganismDoesNotExist()

        return ImageOrganismSerializer(imageOrg).data
