from django.db import models
from django.contrib.auth.models import User
import uuid


class Genre(models.Model):
    genre = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.genre


class Cast(models.Model):
    name = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=50)
    img = models.CharField(max_length=200)

    def __str__(self):
        return '%s: %s : %s' % (self.name, self.role, self.img)


class Drama(models.Model):
    title = models.CharField(max_length=80, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=40, default='Kdrama')
    rating = models.FloatField()
    img = models.URLField()
    year = models.SmallIntegerField(blank=True)
    ua = models.SmallIntegerField(blank=True)
    seasons = models.SmallIntegerField(blank=True)
    poster = models.URLField(blank=True)
    link = models.CharField(max_length=250, default=None)
    # related_name neccessary for serialization relations
    genres = models.ManyToManyField(Genre, related_name="genres", blank=True)
    casts = models.ManyToManyField(Cast, related_name="casts", blank=True)

    def __str__(self):
        return self.title


class Episode(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    description = models.CharField(max_length=200)
    video = models.URLField()
    title = models.CharField(max_length=50, blank=True)
    thumbnailLink = models.URLField(blank=True)
    header = models.CharField(max_length=100, blank=True)
    drama = models.ForeignKey(
        Drama, related_name='episode', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Like(models.Model):
    drama = models.ForeignKey(Drama, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class DramaList(models.Model):
    drama = models.ForeignKey(Drama, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Room(models.Model):
    room = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    video = models.CharField(max_length=1000)
    private = models.BooleanField(default=False)
