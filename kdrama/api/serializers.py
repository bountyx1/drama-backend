from rest_framework import serializers
from .models import Drama, Genre, Cast, Episode, Like, DramaList, Room
from django_restql.mixins import DynamicFieldsMixin
from django.contrib.auth.models import User
from uuid import uuid1


class UserSerializer(serializers.ModelSerializer):
    # Password write only can't view in response
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    # password field must be encrypted and saved using set_password

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]


class CastSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Cast
        fields = '__all__'


class GenreSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre']


class DramaSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    # Be careful not to put it next time in meta class
    genres = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='genre')
    casts = CastSerializer(many=True)

    class Meta:
        model = Drama
        fields = ['id', 'title', 'description', 'link', 'category', 'rating',
                  'img', 'poster', 'year', 'ua', 'seasons', 'genres', 'casts']


class EpisodeSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ["id", "url", "video", "title", "header",
                  "description", "thumbnailLink", "drama"]


class LikeSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class DramaListSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = DramaList
        fields = "__all__"


class RoomSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
