from rest_framework import viewsets, filters
from .serializers import (
    DramaSerializer, GenreSerializer,
    EpisodeSerializer, UserSerializer,
    CastSerializer, WatchListSerializer,
    LikeSerializer, RoomSerializer)
from .models import Drama, Genre, Cast, Episode, Like, WatchList, Room
from .helper import get_drive_link, Drama as ExtractDrama, DramaCool
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.http import HttpResponse


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
    stream = request.GET.get("stream")
    vid = request.GET.get("vid")
    url = get_drive_link(vid, stream)
    response = {"url": url}
    return Response(response)


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
