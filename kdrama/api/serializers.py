from rest_framework import serializers
from .models import Drama, Genre, Cast, Episode, Like, WatchList, Room
from django_restql.mixins import DynamicFieldsMixin
from django.contrib.auth.models import User
from uuid import uuid1


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

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
    genres = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='genre')
    casts = CastSerializer(many=True)

    class Meta:
        model = Drama
        fields = "__all__"


class EpisodeSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = "__all__"


class LikeSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class WatchListSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = "__all__"


class RoomSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
