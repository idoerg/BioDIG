'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for Tag Groups.
    
    Created on January 13, 2013

    @author: Andrew Oberlin
'''
from django import forms
from biodig.base.models import TagGroup
from biodig.base.serializers import TagGroupSerializer

class MultiGetForm(forms.Form):

    def clean(self):
        '''
            Cleans the data for this form to normalize parameters.
        '''
        return self.cleaned_data

    def submit(self):
        '''
            Submits the form for getting multiple TagGroups
            once the form has cleaned the input data.
        '''
        groups = None

        return TagGroupSerializer(groups, many=True).data

class PostForm(forms.Form):

    def clean(self):
        '''
            Cleans the data for this form to normalize parameters.
        '''
        return self.cleaned_data

    def submit(self):
        '''
            Submits the form for creating a TagGroup
            once the form has cleaned the input data.
        '''
        group = None

        return TagGroupSerializer(group).data

class DeleteForm(forms.Form):

    def clean(self):
        '''
            Cleans the data for this form to normalize parameters.
        '''
        return self.cleaned_data

    def submit(self):
        '''
            Submits the form for deleting a TagGroup
            once the form has cleaned the input data.
        '''
        group = None

        return TagGroupSerializer(group).data

class PutForm(forms.Form):

    def clean(self):
        '''
            Cleans the data for this form to normalize parameters.
        '''
        return self.cleaned_data

    def submit(self):
        '''
            Submits the form for updating a TagGroup
            once the form has cleaned the input data.
        '''
        group = None

        return TagGroupSerializer(group).data

class SingleGetForm(forms.Form):

    def clean(self):
        '''
            Cleans the data for this form to normalize parameters.
        '''
        return self.cleaned_data

    def submit(self):
        '''
            Submits the form for getting a TagGroup
            once the form has cleaned the input data.
        '''
        group = None

        return TagGroupSerializer(group).data
