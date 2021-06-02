from rest_framework import permissions, viewsets, filters
from .serializers import DramaSerializer, GenreSerializer, EpisodeSerializer, UserSerializer, CastSerializer, DramaListSerializer, LikeSerializer, RoomSerializer
from .models import Drama, Genre, Cast, Episode, Like, DramaList, Room
from .helper import get_drive_link, Drama as ExtractDrama, DramaCool
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.shortcuts import redirect
from django.http import HttpResponse


class DramaViewSet(viewsets.ModelViewSet):
    #permission_classes = [permissions.IsAuthenticated]
    queryset = Drama.objects.all()
    serializer_class = DramaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'rating']
    # foregin key double underscore notation
    search_fields = ['title', "genres__genre"]


class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CastViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Cast.objects.all()
    serializer_class = CastSerializer


class UserViewSet(viewsets.ViewSet):

    def list(self, request):
        user = self.request.user
        queryset = User.objects.filter(username=user.username)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        response = {}
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response["success"] = serializer.data
            return Response(response)
        else:
            response["errors"] = serializer.errors
            return Response(response)


class DramaListViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = self.request.user
        queryset = DramaList.objects.filter(user__username=user)
        serializer = DramaListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = self.request.user
        queryset = DramaList.objects.filter(
            drama=pk).filter(user__username=user)
        serializer = DramaListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = self.request.user
        data = request.data
        data["user"] = user.id
        check = DramaList.objects.filter(
            drama=data["drama"]).filter(user=user.id).exists()
        if not check:
            serializer = DramaListSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({"status": "failed", "err": "Internal Server Error"})
        else:
            return Response({"status": "failed", "err": "Already Exists"})

    def destroy(self, request, pk=None):
        user = self.request.user
        item = DramaList.objects.filter(drama=pk).filter(user__username=user)
        item.delete()
        return Response(status=204)


class LikeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        queryset = Like.objects.filter(user__username=user)
        serializer = LikeSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = self.request.user
        queryset = Like.objects.filter(drama=pk).filter(user__username=user)
        serializer = LikeSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = self.request.user
        data = request.data
        data["user"] = user.id
        check = Like.objects.filter(
            drama=data["drama"]).filter(user=user.id).exists()
        if not check:
            serializer = LikeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({"status": "failed", "err": "Internal Server Error"})
        else:
            return Response({"status": "failed", "err": "Already Exists"})

    def destroy(self, request, pk=None):
        user = self.request.user
        item = Like.objects.filter(drama=pk).filter(user__username=user)
        item.delete()
        return Response(status=204)


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


'''
    @method_decorator(cache_page(60*60))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
'''


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['room']


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
