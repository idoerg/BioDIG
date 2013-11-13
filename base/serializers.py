'''
Created on Nov 3, 2013

@author: Andrew Oberlin
'''
from models import TagGroup
from rest_framework import serializers

class TagGroupSerializer(serializers.ModelSerializer):
    image = serializers.PrimaryKeyRelatedField(source='picture')
    
    class Meta:
        model = TagGroup
        fields = ('id', 'name', 'image', 'user', 'dateCreated', 'lastModified', 'isPrivate')
