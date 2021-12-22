from django.db import models
from django.contrib.auth.models import User
import uuid


class Genre(models.Model):
    genre = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.genre


class Cast(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    img = models.URLField(max_length=500)

    def __str__(self):
        return self.name


class Drama(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    country = models.CharField(max_length=40, null=True, blank=True)
    rating = models.FloatField(default=0.0)
    img = models.URLField(blank=True, null=True)
    year = models.SmallIntegerField(default=0000)
    ua = models.SmallIntegerField(blank=True, null=True)
    seasons = models.SmallIntegerField(blank=True, default=1)
    poster = models.URLField(blank=True)
    link = models.CharField(max_length=250, blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name="genres", blank=True)
    casts = models.ManyToManyField(Cast, related_name="casts", blank=True)

    def __str__(self):
        return self.title


class Episode(models.Model):
    title = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    video = models.URLField(blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)
    header = models.CharField(max_length=100, blank=True)
    drama = models.ForeignKey(
        Drama, related_name='episode', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Like(models.Model):
    drama = models.ForeignKey(Drama, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class WatchList(models.Model):
    drama = models.ForeignKey(Drama, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    video = models.CharField(max_length=1000)
    private = models.BooleanField(default=False)
