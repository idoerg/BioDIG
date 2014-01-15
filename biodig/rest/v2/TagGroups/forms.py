'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for Tag Groups.
    
    Created on January 13, 2013

    @author: Andrew Oberlin
'''
from django import forms
from biodig.base.models import TagGroup
from biodig.base.util import Util
from biodig.base.serializers import TagGroupSerializer

class MultiGetForm(forms.Form):
    # Query Parameters
    offset = forms.IntegerField(required=False)
    limit = forms.IntegerField(required=False)
    # Tag Group filters
    lastModified = Util.DateTimeRangeField(required=False)
    dateCreated = Util.DateTimeRangeField(required=False)
    user = forms.IntegerField(required=False)
    image = forms.IntegerField(required=False)
    name = forms.CharField(required=False)

    def clean(self):
        if not self.cleaned_data['offset']: self.cleaned_data['offset'] = 0
        return self.cleaned_data


    def submit(self, request):
        '''
            Submits the form for getting multiple TagGroups
            once the form has cleaned the input data.
        '''
        query = TagGroup.objects.all()
        
        # add permissions to query
        if request.user and request.user.is_authenticated():
            if not request.user.is_staff:
                query = query.filter(isPrivate = False) | TagGroup.objects.filter(user__pk__exact=request.user.pk)
        else:
            query = query.filter(isPrivate=False)
        
        # if a name was given then we will filter by it
        if self.cleaned_data['name']: query = query.filter(name__in=self.cleaned_data['name'])
        
        if self.cleaned_data['image']: query = query.filter(picture__pk__in=self.cleaned_data['image'])
            
        if self.cleaned_data['user']: query = query.filter(user__pk__in=self.cleaned_data['user'])
            
        if self.cleaned_data['lastModified']:
            query = query.filter(**self.cleaned_data['lastModified'].filterParams())
            
        if self.cleaned_data['dateCreated']:
            query = query.filter(**self.cleaned_data['dateCreated'].filterParams())
            
        if not self.cleaned_data['limit'] or self.cleaned_data['limit'] < 0:
            query = query[self.cleaned_data['offset']:]
        else:
            query = query[self.cleaned_data['offset'] : self.cleaned_data['offset']+self.cleaned_data['limit']]

        return TagGroupSerializer(query, many=True).data

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
