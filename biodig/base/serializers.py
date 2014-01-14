'''
Created on Nov 3, 2013

@author: Andrew Oberlin
'''
from models import TagGroup
from rest_framework import serializers
import biodig.swagger.decorators.Models as Models
import biodig.swagger.decorators.Types as Types

@Models.Property('id', Types.Integer)
@Models.Property('name', Types.String)
@Models.Property('image', Types.Integer)
@Models.Property('user', Types.Integer)
@Models.Property('dateCreated', Types.Date)
@Models.Property('lastModified', Types.Date)
@Models.Property('isPrivate', Types.Boolean)
class TagGroupSerializer(serializers.ModelSerializer):
    image = serializers.PrimaryKeyRelatedField(source='picture')
    
    class Meta:
        model = TagGroup
        fields = ('id', 'name', 'image', 'user', 'dateCreated', 'lastModified', 'isPrivate')
