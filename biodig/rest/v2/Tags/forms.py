'''
    This file holds all of the forms for the cleaning and validation of
    the parameters being used for Tags.
    
    Created on February 10, 2013

    @author: Andrew Oberlin
'''
from django import forms
from biodig.base.models import Tag, TagColor, TagPoint, TagGroup, Picture
from biodig.base import forms as bioforms
from biodig.base.serializers import TagSerializer
from biodig.base.exceptions import TagDoesNotExist, DatabaseIntegrity, TagGroupDoesNotExist
from rest_framework.exceptions import PermissionDenied
from django.db import transaction, DatabaseError
from django.core.exceptions import ValidationError
import numbers

class FormCleaningUtil:
    @staticmethod
    def clean_image_id(data):
        '''
            Checks that the image_id is a positive integer.
        '''
        if data['image_id'] < 0: raise ValidationError("The given image id is incorrect.")
        return data['image_id']
    
    @staticmethod
    def clean_tag_group_id(data):
        '''
            Checks that the tag_group_id is a positive number..
        '''
        if data['tag_group_id'] < 0: raise ValidationError("The given tag group id is incorrect.")
        return data['tag_group_id']
    
    @staticmethod
    def clean_tag_id(data):
        '''
            Checks that the tag_id is a positive number..
        '''
        if data['tag_id'] < 0: raise ValidationError("The given tag id is incorrect.")
        return data['tag_id']

    @staticmethod
    def clean_points(data):
        '''
            Checks that the JSONField produced the correct structure for each
            point.
        '''
        # check that the points are an array
        if not isinstance(data['points'], list):
            raise ValidationError("A valid JSON array should be given for points parameter") 

        # check if points array is 2 points or more in length
        if len(data['points']) < 2:
            raise ValidationError("List of points should be at least length two")

        for point in data['points']:
            if 'x' not in point or 'y' not in point:
                raise ValidationError("Each point should be given as a dictionary with keys x and y")
            if not isinstance(point['x'], numbers.Number):
                raise ValidationError("The x-value of a point must be a number")
            if not isinstance(point['y'], numbers.Number):
                raise ValidationError("The y-value of a point must be a number")

        return data['points']
    
    @staticmethod
    def clean_color(data):
        if not isinstance(data['color'], dict):
            raise ValidationError("A valid JSON dictionary should be given for color parameter")
        color = {}
        accepted = { 'r', 'g', 'b' }
        for key, val in data['color'].iteritems():
            if key in accepted:
                if not isinstance(val, int) or val < 0 or val > 255:
                    raise ValidationError("Value for key " + key + " is not an integer between 0 and 255")
                accepted.remove(key)
                color[key] = val
                
        if accepted: # missingkeys for color
            raise ValidationError("The keys " + ", ".join(list(accepted)) + "were missing from the color")
        
        return color

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

    def clean_image_id(self):
        return FormCleaningUtil.clean_image_id(self.cleaned_data)

    def clean_tag_group_id(self):
        return FormCleaningUtil.clean_tag_group_id(self.cleaned_data)

    def clean_points(self):
        return FormCleaningUtil.clean_points(self.cleaned_data)
    
    def clean_color(self):
        return FormCleaningUtil.clean_color(self.cleaned_data)
    
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
        
        # create tag points
        points = []
        for counter, point in enumerate(self.cleaned_data['points']):
            points.append(TagPoint(pointX=float(point['x']), pointY=float(point['y']), rank=counter+1))

        # create the tag's color
        color = self.cleaned_data['color']
        color = TagColor.objects.get_or_create(red=int(color['r']), green=int(color['g']), blue=int(color['b']))[0]

        # start saving the new tag now that it has passed all tests
        tag = Tag(name=self.cleaned_data['name'], color=color, group=group, user=request.user)
        try:
            tag.save()
            for point in points:
                point.tag = tag
                point.save()
        except DatabaseError:
            transaction.rollback()
            raise DatabaseIntegrity()

        return TagSerializer(tag, points).data

class DeleteForm(forms.Form):
    image_id = forms.IntegerField(required=True)
    tag_group_id = forms.IntegerField(required=True)
    tag_id = forms.IntegerField(required=True)

    def clean_tag_id(self):
        return FormCleaningUtil.clean_tag_id(self.cleaned_data)

    def clean_tag_group_id(self):
        return FormCleaningUtil.clean_tag_group_id(self.cleaned_data)
    
    def clean_image_id(self):
        return FormCleaningUtil.clean_image_id(self.cleaned_data)
    
    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for deleting a TagGroup
            once the form has cleaned the input data.
        '''
        try:
            group = TagGroup.objects.get(pk__exact=self.cleaned_data['tag_group_id'], picture__exact=self.cleaned_data['image_id'])
            if not request.user.is_staff and group.user != request.user:
                raise PermissionDenied()
        except (TagGroup.DoesNotExist, ValueError):
            raise TagGroupDoesNotExist()
        try:
            tag = Tag.objects.get(pk__exact=self.cleaned_data['tag_id'], group=group)
            if not request.user.is_staff and tag.user != request.user:
                raise PermissionDenied()
        except Tag.DoesNotExist:
            raise TagDoesNotExist()
        
        points = TagPoint.objects.filter(tag=tag)
        serialized = TagSerializer(tag, points).data
        
        try:
            tag.delete()
            points.delete()
        except DatabaseError:
            transaction.rollback()
            raise DatabaseIntegrity()
        
        return serialized

class PutForm(forms.Form):
    image_id = forms.IntegerField(required=True)
    tag_group_id = forms.IntegerField(required=True)
    tag_id = forms.IntegerField(required=True)
    name = forms.CharField(required=False)
    points = bioforms.JsonField(required=False)
    color = bioforms.JsonField(required=False)

    def clean_tag_id(self):
        return FormCleaningUtil.clean_tag_id(self.cleaned_data)

    def clean_tag_group_id(self):
        return FormCleaningUtil.clean_tag_group_id(self.cleaned_data)
    
    def clean_image_id(self):
        return FormCleaningUtil.clean_image_id(self.cleaned_data)
    
    def clean_points(self):
        return FormCleaningUtil.clean_points(self.cleaned_data) if self.cleaned_data['points'] else None
    
    def clean_color(self):
        return FormCleaningUtil.clean_color(self.cleaned_data) if self.cleaned_data['color'] else None

    @transaction.commit_on_success
    def submit(self, request):
        '''
            Submits the form for updating a Tag
            once the form has cleaned the input data.
        '''
        try:
            group = TagGroup.objects.get(pk__exact=self.cleaned_data['tag_group_id'], picture__exact=self.cleaned_data['image_id'])
            if not request.user.is_staff and group.user != request.user:
                raise PermissionDenied()
        except (TagGroup.DoesNotExist, ValueError):
            raise TagGroupDoesNotExist()
        try:
            tag = Tag.objects.get(pk__exact=self.cleaned_data['tag_id'], group=group)
            if not request.user.is_staff and tag.user != request.user:
                raise PermissionDenied()
        except Tag.DoesNotExist:
            raise TagDoesNotExist()
        
        try:
            changed = False
            
            if self.cleaned_data['color']:
                # update color
                color = self.cleaned_data['color']
                color = TagColor.objects.get_or_create(red=int(color['r']), green=int(color['g']), blue=int(color['b']))[0]
                tag.color = color
                changed = True
            
            if self.cleaned_data['name']:
                # update the name
                tag.name = self.cleaned_data['name']
                changed = True
            
            points = None
            if self.cleaned_data['points']:
                # update points and delete old points
                # create tag points
                points = []
                for counter, point in enumerate(self.cleaned_data['points']):
                    point = TagPoint(tag=tag, pointX=float(point['x']), pointY=float(point['y']), rank=counter+1)
                    points.append(point)
                changed = True
                
            if changed:
                tag.save()
                if points is not None: # we have points
                    TagPoint.objects.filter(tag=tag).delete() # deletes all the old tag points
                    for point in points:
                        point.save()        
        except DatabaseError:
            transaction.rollback()
            raise DatabaseIntegrity()
            
        return TagSerializer(tag, points).data

class SingleGetForm(forms.Form):
    image_id = forms.IntegerField(required=True)
    tag_group_id = forms.IntegerField(required=True)
    tag_id = forms.IntegerField(required=True)
    def clean_tag_id(self):
        return FormCleaningUtil.clean_tag_id(self.cleaned_data)

    def clean_tag_group_id(self):
        return FormCleaningUtil.clean_tag_group_id(self.cleaned_data)
    
    def clean_image_id(self):
        return FormCleaningUtil.clean_image_id(self.cleaned_data)

    def submit(self, request):
        '''
            Submits the form for getting a Tag
            once the form has cleaned the input data.
        '''
        try:
            group = TagGroup.objects.get(pk__exact=self.cleaned_data['tag_group_id'], picture__exact=self.cleaned_data['image_id'])
            if group.isPrivate and not request.user.is_staff and group.user != request.user:
                raise PermissionDenied()
        except (TagGroup.DoesNotExist, ValueError):
            raise TagGroupDoesNotExist()
        try:
            tag = Tag.objects.get(pk__exact=self.cleaned_data['tag_id'], group=group)
            if tag.isPrivate and not request.user.is_staff and tag.user != request.user:
                raise PermissionDenied()
        except Tag.DoesNotExist:
            raise TagDoesNotExist()

        return TagSerializer(tag).data
