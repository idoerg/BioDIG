'''
Created on Nov 3, 2013

@author: Andrew Oberlin
'''
from models import Picture, TagGroup, Tag, TagPoint
from rest_framework import serializers
import biodig.swagger.decorators.Models as Models
import biodig.swagger.decorators.Types as Types

class ImageSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='imageName')
    owner = serializers.PrimaryKeyRelatedField(source='user')
    dateCreated = serializers.DateTimeField(source='uploadDate')
    
    class Meta:
        model = Picture
        fields = ('id', 'description', 'url', 'thumbnail', 'owner', 'dateCreated', 'altText')

@Models.Property('id', Types.Integer)
@Models.Property('name', Types.String)
@Models.Property('image', Types.Integer)
@Models.Property('owner', Types.Integer)
@Models.Property('dateCreated', Types.Date)
@Models.Property('lastModified', Types.Date)
@Models.Property('isPrivate', Types.Boolean)
class TagGroupSerializer(serializers.ModelSerializer):
    image = serializers.PrimaryKeyRelatedField(source='picture')
    owner = serializers.PrimaryKeyRelatedField(source='user')
    
    class Meta:
        model = TagGroup
        fields = ('id', 'name', 'image', 'owner', 'dateCreated', 'lastModified', 'isPrivate')
        
        
class TagSerializer:
    def __init__(self, tag, points=None, many=False):
        self.data = SecretTagSerializer(tag, many=many).data
        if not many:
            if points is None:
                points = TagPoint.objects.filter(tag__exact=tag)
            self.data['points'] = TagPointSerializer(points, many=True).data
        else:
            for index, tag in enumerate(self.data):
                points = TagPoint.objects.filter(tag__exact=tag['id'])
                tag['points'] = TagPointSerializer(points, many=True).data
                self.data[index] = tag
                
            

class TagPointSerializer(serializers.ModelSerializer):
    x = serializers.FloatField(source='pointX')
    y = serializers.FloatField(source='pointY')

    class Meta:
        model = TagPoint
        fields = ('x', 'y', 'rank')

@Models.Property('id', Types.Integer)
@Models.Property('name', Types.String)
@Models.Property('group', Types.Integer)
@Models.Property('owner', Types.Integer)
@Models.Property('color', Types.String)
@Models.Property('dateCreated', Types.Date)
@Models.Property('lastModified', Types.Date)
@Models.Property('isPrivate', Types.Boolean)
class SecretTagSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(source='user')
    
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'group', 'owner', 'dateCreated', 'lastModified', 'isPrivate')
