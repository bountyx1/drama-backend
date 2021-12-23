from requests.api import head
from rest_framework import viewsets, filters
from .serializers import (
    DramaSerializer, GenreSerializer,
    EpisodeSerializer, UserSerializer,
    CastSerializer, WatchListSerializer,
    LikeSerializer, RoomSerializer)
from .models import Drama, Genre, Cast, Episode, Like, WatchList, Room
from .helper import Drama as ExtractDrama, DramaCool
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.http import HttpResponse
import requests
from urllib.parse import  parse_qs



class DramaViewSet(viewsets.ModelViewSet):
    queryset = Drama.objects.all()
    serializer_class = DramaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['country', 'rating']
    search_fields = ['title', "genres__genre"]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CastViewSet(viewsets.ModelViewSet):
    queryset = Cast.objects.all()
    serializer_class = CastSerializer


class WatchListViewSet(viewsets.ModelViewSet):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['room']


class EpisodeViewSet(viewsets.ModelViewSet):
    serializer_class = EpisodeSerializer

    def get_queryset(self):
        dramaid = self.request.GET.get("dramaid")
        if dramaid is not None:
            drama = Drama.objects.get(id=dramaid)
            url = "https://dramacool.ch"+drama.link
            result = ExtractDrama(
                url, headers={"X-Requested-With": "XMLHttpRequest"})
            res = result.run()
            for r in res:
                video, id, title = r
                episode = Episode(id=id, title=title, description="Not Available",
                                  video=video, thumbnailLink="", header="test=none", drama=drama)
                episode.save()
            queryset = Episode.objects.filter(drama=dramaid)
            return queryset


@api_view(['GET'])
def drive(request):
    id = request.GET.get("id")
    key = request.GET.get("key")
    token = request.GET.get("token")
    header = {"Cookie": f"DRIVE_STREAM={token};"}
    driveurl = f"https://drive.google.com/u/0/get_video_info?docid={id}&resourcekey={key}"
    query = requests.get(driveurl, headers=header).text
    media_map = parse_qs(query)["fmt_stream_map"]
    url = media_map[0].split("|")[1].split(",")[0]

    return Response({"url":url})


@api_view(['GET'])
def get_drama(request):
    url = request.GET.get("url")
    url = "https://dramacool.ch"+url
    result = ExtractDrama(url, headers={"X-Requested-With": "XMLHttpRequest"})
    res = result.run()
    return Response(res)


@api_view(['GET'])
def search_drama(request):
    name = request.GET.get('name')
    drama = DramaCool("https://dramacool.com",
                      headers={"X-Requested-With": "XMLHttpRequest"})
    result = drama.search(name)
    return Response(result)


@api_view(['GET'])
def url_redirect(request):
    rdr = request.GET.get('rdr')
    html = f"<script>document.location.href='kdrama://room/{rdr}'; </script>"
    return HttpResponse(html)
