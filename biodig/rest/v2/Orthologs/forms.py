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
from django.db import transaction, DatabaseError
from django.core.exceptions import ValidationError
from django.conf import settings
import csv

class FormUtil:
    @staticmethod
    def clean_TC_id(data):
        '''
            Cleans an user id ensuring that it is a positive integer.
        '''
        TCNum=data['TC_id']
        if TCNum[0:3] !="TC_":
            raise ValidationError("TC id is incorrect.")
        return data['TC_id']

    def Ortholog_Dict():
	'''
		Reads a csv file,
		returns a dict of TC_Num and its orthologs.
        '''
	Ortho_Dict= {}
	f = open(testGen.csv)
        reader= csv.reader(f)
	for i,row in enumerate(reader):
             if i==0:
		header= row
	     else:
		Ortho_Dict[row[0]]=row[1:]  
	return Ortho_Dict

class MultiGetForm(forms.Form):

    def clean(self):
        if not self.cleaned_data['offset']: self.cleaned_data['offset'] = 0
        return self.cleaned_data


    def submit(self, request):
        '''
            Submits the form for getting multiple Organisms
            once the form has cleaned the input data.
        '''
	Ortho_Dict= FormUtil.Ortholog_Dict()
        return Ortho_Dict


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
        try:
            Ortho_Dict = FormUtil.Ortholog_Dict()
	    Ortho_list=Ortho_Dict[self.cleaned_data['TC_id']]
        except (Ortholog.DoesNotExist, ValueError):
            raise OrthologDoesNotExist()

        return Ortho_list


