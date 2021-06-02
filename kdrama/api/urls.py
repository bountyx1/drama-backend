from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'dramas', views.DramaViewSet)
router.register(r'genre', views.GenreViewSet)
router.register(r'casts', views.CastViewSet)
router.register(r'users', views.UserViewSet, basename="user")
router.register(r'likes', views.LikeViewSet, basename="like")
router.register(r'watchlist', views.DramaListViewSet, basename="watchlist")
router.register(r'rooms', views.RoomViewSet, basename='room')
# Basename set ViewName with s
router.register(r'episodes', views.EpisodeViewSet, basename="episode")

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('drive', views.drive),
    path('video', views.get_drama),
    path('search', views.search_drama),
    path('redirect', views.url_redirect),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
