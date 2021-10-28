from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

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


class AlbumViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet,):

    queryset = User.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (IsAlbumOwner, permissions.IsAuthenticated)

    def get_queryset(self):
        return self.request.user.images.all()

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class ImageDetailViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def _get_image(self):
        image = get_object_or_404(Image, id=self.kwargs['image_id'])
        image.views = image.views + 1
        image.save(update_fields=('views',))
        return image

    def get_queryset(self):
        self._get_image()
        queryset = Image.objects.filter(id=self.kwargs['image_id'])
        return queryset
