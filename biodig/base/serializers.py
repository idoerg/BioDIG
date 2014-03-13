'''
Created on Nov 3, 2013

@author: Andrew Oberlin
'''
from models import Picture, TagGroup, Tag
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
        
        
@Models.Property('id', Types.Integer)
@Models.Property('name', Types.String)
@Models.Property('group', Types.Integer)
@Models.Property('owner', Types.Integer)
@Models.Property('color', Types.String)
@Models.Property('dateCreated', Types.Date)
@Models.Property('lastModified', Types.Date)
@Models.Property('isPrivate', Types.Boolean)
class TagSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(source='user')
    
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'group', 'owner', 'dateCreated', 'lastModified', 'isPrivate')
