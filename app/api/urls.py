from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import AlbumViewSet, RegisterApi, ImageDetailViewSet


router = DefaultRouter()
router.register(r'album', AlbumViewSet)
router.register(r'album/image', ImageDetailViewSet)

app_name = 'api'

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/register/', RegisterApi.as_view()),
    path('v1/token/create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]