'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for Orthologs (based on "Organisms").

    Created on May 26, 2014

    @author: Asma
'''
from django import forms
from biodig.base import forms as bioforms
from biodig.base.exceptions import OrthologDoesNotExist
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
import csv
from django.conf import settings
import os

class FormUtil:
    @staticmethod
    def clean_TC_id(data):
        '''
            Cleans an user id ensuring that it is a positive integer.
        '''
        TCNum = data['TC_id']
        if len(TCNum) <= 2 or TCNum[:2] != "TC":
            raise ValidationError("TC id is incorrect.")
        return data['TC_id']

    @staticmethod
    def ortholog_dict(filePath):
	'''
	    Reads a csv file,
	    returns a dict of TC_Num and its orthologs.
        '''
	ortho_dict= {}
	with open(os.path.join(settings.PROJECT_PATH, filePath), 'r') as f:
            reader= csv.reader(f)
	    for i,row in enumerate(reader):
                if i == 0:
                    header = row
	        else:
                    ortho_dict[row[0]] = row[1:]  
	
        return ortho_dict

class MultiGetForm(forms.Form):

    def submit(self, request):
        '''
            Submits the form for getting multiple Organisms
            once the form has cleaned the input data.
        '''
	ortho_dict = FormUtil.ortholog_dict('data/testGen.csv')
        ortho_dict1 = FormUtil.ortholog_dict('data/orthoDB.csv')
        return ortho_dict, ortho_dict1


class SingleGetForm(forms.Form):
    # Path Parameters
    TC_id = forms.CharField(required=True)

    def clean_TC_id(self):
        return FormUtil.clean_TC_id(self.cleaned_data)

    def submit(self, request):
        '''
            Submits the form for getting a Organism
            once the form has cleaned the input data.
        '''
        final_dict = {}
        try:
            ortho_dict = FormUtil.ortholog_dict('data/testGen.csv')
            ortho_dict1 = FormUtil.ortholog_dict('data/orthoDB.csv')
	    ortho_list = ortho_dict[self.cleaned_data['TC_id']]
            ortho_list1 = ortho_dict1[self.cleaned_data['TC_id']]
            final_dict["FlyBase"] = ortho_list;
            final_dict["OrthoDB"] = ortho_list1;
        except KeyError:
            raise OrthologDoesNotExist()

        return final_dict


