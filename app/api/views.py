from rest_framework import permissions, viewsets, generics
from rest_framework.response import Response

from .models import Image, User
from .permissions import IsAlbumOwner
from .serializers import ImageSerializer, RegisterSerializer, UserSerializer


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'message': 'User successfully added.',
        })


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (IsAlbumOwner, permissions.IsAuthenticated)

    def get_queryset(self):
        return self.request.user.images.all()

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = (IsAlbumOwner,)

    def get_queryset(self):
        return self.request.user.images.all()
