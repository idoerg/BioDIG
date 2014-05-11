'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for Tag Groups.

    Created on January 13, 2013

    @author: Andrew Oberlin
'''
from django import forms
from biodig.base.models import Organism, Feature
from biodig.base import forms as bioforms
from biodig.base.serializers import OrganismSerializer, FeatureSerializer
from biodig.base.exceptions import OrganismDoesNotExist, FeatureDoesNotExist, DatabaseIntegrity
from rest_framework.exceptions import PermissionDenied
from django.db import transaction, DatabaseError
from django.core.exceptions import ValidationError
from django.conf import settings

class FormUtil:
    @staticmethod
    def clean_organism_id(data):
        '''
            Cleans an user id ensuring that it is a positive integer.
        '''
        if data['organism_id'] < 0:
            raise ValidationError("Organism id is incorrect.")
        return data['organism_id']

class MultiGetForm(forms.Form):
    # Query Parameters
    offset = forms.IntegerField(required=False)
    limit = forms.IntegerField(required=False)
    # Organism filters (Query)
    common_name = forms.CharField(required=False)
    genus = forms.CharField(required=False)
    species = forms.CharField(required=False)

    def clean(self):
        if not self.cleaned_data['offset']: self.cleaned_data['offset'] = 0
        return self.cleaned_data


    def submit(self, request):
        '''
            Submits the form for getting multiple Organisms
            once the form has cleaned the input data.
        '''
        qbuild = bioforms.QueryBuilder(Organism)

        filterkeys = [
            'common_name', 'genus', 'species'
        ]
        for key in filterkeys:
            qbuild.filter(key, self.cleaned_data[key])

        if not self.cleaned_data['limit'] or self.cleaned_data['limit'] < 0:
            qbuild.q = qbuild()[self.cleaned_data['offset']:]
        else:
            qbuild.q = qbuild()[self.cleaned_data['offset'] : self.cleaned_data['offset']+self.cleaned_data['limit']]

        return OrganismSerializer(qbuild(), many=True).data


class SingleGetForm(forms.Form):
    # Path Parameters
    organism_id = forms.IntegerField(required=True)

    def clean_organism_id(self):
        return FormUtil.clean_organism_id(self.cleaned_data)

    def submit(self, request):
        '''
            Submits the form for getting a Organism
            once the form has cleaned the input data.
        '''
        try:
            organism = Organism.objects.get(pk__exact=self.cleaned_data['organism_id'])
        except (Organism.DoesNotExist, ValueError):
            raise OrganismDoesNotExist()

        return OrganismSerializer(organism).data

class FeatureMultiGetForm(forms.Form):
    # Path Parameters
    organism_id = forms.IntegerField(required=True)

    def clean_organism_id(self):
        return FormUtil.clean_organism_id(self.cleaned_data)

    def submit(self, request):
        '''
            Submits the form for getting an Organism's Feature list
            once the form has cleaned the input data.
        '''
        try:
            organism = Organism.objects.get(pk__exact=self.cleaned_data['organism_id'])
        except (Organism.DoesNotExist, ValueError):
            raise OrganismDoesNotExist()

        try:
            features = Feature.objects.filter(organism=organism)
        except Feature.DoesNotExist:
            raise FeatureDoesNotExist()

        return FeatureSerializer(features, many=True).data
