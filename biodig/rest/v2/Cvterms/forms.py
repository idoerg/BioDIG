'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for Tag Groups.

    Created on January 13, 2013

    @author: Andrew Oberlin
'''
from django import forms
import biodig.base.forms as bioforms
from biodig.base.models import Cvterm, Cv
from biodig.base.serializers import CvtermSerializer
from biodig.base.exceptions import CvDoesNotExist, DatabaseIntegrity
from rest_framework.exceptions import PermissionDenied
from django.db import transaction, DatabaseError
from django.core.exceptions import ValidationError
from django.conf import settings

class FormUtil:
    @staticmethod
    def clean_cvterm_id(data):
        '''
            Cleans an cvterm id ensuring that it is a positive integer.
        '''
        if data['cvterm_id'] < 0:
            raise ValidationError("Cvterm id is incorrect.")
        return data['cvterm_id']

class MultiGetForm(forms.Form):
    # Path Parameters
    cv = forms.CharField(required=True)

    # Query Parameters
    offset = forms.IntegerField(required=False)
    limit = forms.IntegerField(required=False)

    # term filters (Query)
    name = forms.CharField(required=False)
    is_relationshiptype = forms.CharField(required=False)
    is_obsolete = forms.CharField(required=False)

    def clean(self):
        raise DatabaseIntegrity(detail=self.cleaned_data['is_relationshiptype'])
        is_rel = self.cleaned_data['is_relationshiptype'].lower()
        if is_rel:
            converted = 1 if is_rel == "true" else (0 if is_rel == "false" else None)
            self.cleaned_data['is_relationshiptype'] = converted
        else:
            self.cleaned_data['is_relationshiptype'] = None

        is_obs = self.cleaned_data['is_obsolete'].lower()
        if is_obs:
            converted = 1 if is_obs == "true" else (0 if is_obs == "false" else None)
            self.cleaned_data['is_obsolete'] = converted
        else:
            self.cleaned_data['is_obsolete'] = None

        if not self.cleaned_data['offset']: self.cleaned_data['offset'] = 0
        return self.cleaned_data


    def submit(self, request):
        '''
            Submits the form for getting multiple Cvterms
            once the form has cleaned the input data.
        '''
        qbuild = bioforms.QueryBuilder(Cvterm)

        try:
            self.cleaned_data['cv'] = Cv.objects.get(name=self.cleaned_data['cv'])
        except Cv.DoesNotExist:
            raise CvDoesNotExist()

        filterkeys = ['name', 'cv']
        for key in filterkeys:
            qbuild.filter(key, self.cleaned_data[key])

        if self.cleaned_data['is_relationshiptype'] is not None:
            qbuild.filter('is_relationshiptype', self.cleaned_data['is_relationshiptype'])

        if self.cleaned_data['is_obsolete'] is not None:
            qbuild.filter('is_obsolete', self.cleaned_data['is_obsolete'])

        if not self.cleaned_data['limit'] or self.cleaned_data['limit'] < 0:
            qbuild.q = qbuild()[self.cleaned_data['offset']:]
        else:
            qbuild.q = qbuild()[self.cleaned_data['offset'] : self.cleaned_data['offset']+self.cleaned_data['limit']]

        return CvtermSerializer(qbuild(), many=True).data


class SingleGetForm(forms.Form):
    # Path Parameters
    cvterm_id = forms.IntegerField(required=True)
    cv = forms.CharField(required=True)

    def clean_cvterm_id(self):
        return FormUtil.clean_cvterm_id(self.cleaned_data)

    def submit(self, request):
        '''
            Submits the form for getting a Cvterm
            once the form has cleaned the input data.
        '''
        try:
            cv = Cv.objects.get(name=self.cleaned_data['cv'])
        except Cv.DoesNotExist:
            raise CvDoesNotExist()

        try:
            term = Cvterm.objects.get(pk__exact=self.cleaned_data['cvterm_id'], cv=cv)
        except (Cvterm.DoesNotExist, ValueError):
            raise CvtermDoesNotExist()

        return CvtermSerializer(term).data
