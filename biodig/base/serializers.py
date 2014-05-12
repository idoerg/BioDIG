'''
Created on Nov 3, 2013

@author: Andrew Oberlin
'''
from django.contrib.auth.models import User
from models import Image, TagGroup, Tag, TagPoint, TagColor, GeneLink, Organism, Feature
from rest_framework import serializers
import biodig.swagger.decorators.Models as Models
import biodig.swagger.decorators.Types as Types

class ImageSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='imageName')
    owner = serializers.PrimaryKeyRelatedField(source='user')
    dateCreated = serializers.DateTimeField(source='uploadDate')

    class Meta:
        model = Image
        fields = ('id', 'description', 'url', 'thumbnail', 'owner', 'dateCreated', 'altText')

class ImageOrganismSerializer:
    def __init__(self, imageOrg, many=False):
        if not many:
            self.data = OrganismSerializer(imageOrg.organism, many=many).data
        else:
            self.data = OrganismSerializer([org.organism for org in imageOrg], many=many).data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_active')

class OrganismSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='organism_id')

    class Meta:
        model = Organism
        fields = ('id', 'common_name', 'genus', 'species', 'abbreviation')


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

class TagColorSerializer(serializers.ModelSerializer):
    r = serializers.IntegerField(source='red')
    g = serializers.IntegerField(source='green')
    b = serializers.IntegerField(source='blue')
    a = serializers.FloatField(source='alpha')

    class Meta:
        model = TagColor
        fields = ('r', 'g', 'b', 'a')

class SecretTagSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(source='user')
    color = TagColorSerializer()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'group', 'owner', 'dateCreated', 'lastModified', 'isPrivate')

class FeatureTypeField(serializers.RelatedField):
    def to_native(self, value):
        return str(value.name)

class FeatureSerializer(serializers.ModelSerializer):
    type = FeatureTypeField()
    id = serializers.IntegerField(source='feature_id')

    class Meta:
        model = Feature
        fields = ('id', 'name', 'uniquename', 'type')

class CvtermSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='cvterm_id')
    cv = serializers.PrimaryKeyRelatedField(source='cv')

    class Meta:
        model = Feature
        fields = ('id', 'name', 'cv', 'description')

class GeneLinkSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(source='user')
    feature = FeatureSerializer()

    class Meta:
        model = GeneLink
        fields = ('id', 'feature', 'tag', 'dateCreated', 'lastModified', 'owner')
