from django.shortcuts import redirect
from django.urls import include, path
from rest_framework import routers
from .views import (
    DramaViewSet, GenreViewSet, CastViewSet, LikeViewSet,
    WatchListViewSet, RoomViewSet, EpisodeViewSet, UserViewSet,
    get_drama, drive, url_redirect, search_drama
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,TokenRefreshView,
)

router = routers.DefaultRouter()

router.register(r'dramas', DramaViewSet)
router.register(r'genre', GenreViewSet)
router.register(r'casts', CastViewSet)
router.register(r'users', UserViewSet)
router.register(r'likes', LikeViewSet, basename="likes")
router.register(r'watchlist', WatchListViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'episodes', EpisodeViewSet, basename="episodes")

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('drive', drive),
    path('video', get_drama),
    path('search', search_drama),
    path('redirect', url_redirect),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
