from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Image, User
from .permissions import IsAlbumOwner
from .serializers import ImageSerializer, RegisterSerializer, UserSerializer


class RegisterApi(generics.GenericAPIView):
    """
    API view for user sign-up.
    Accepts 'POST' request. Requiered fields: 'username' and 'password'.
    """
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
    """
    This viewset allows 'GET' and 'POST' requests for authorized users.
    User can get a list of all of the photos he posted and post a new one.
    For privacy reasons users are not allowed to view photos of other users.
    """
    queryset = User.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (IsAlbumOwner, permissions.IsAuthenticated)

    def get_queryset(self):
        return self.request.user.images.all()

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class ImageDetailViewSet(mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    This viewset allows 'GET', 'PUT', 'PATCH' and 'DELETE' requests.
    Users can retrieve, edit and delete specific images.
    Retrieving specific image is recorded in 'views' field of the Image model.
    For privacy reasons users are not allowed to view photos of other users.
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.IsAuthenticated, IsAlbumOwner)

    def _get_image(self):
        image = get_object_or_404(Image, id=self.kwargs['pk'])
        image.views = image.views + 1
        image.save(update_fields=('views',))
        return image.id

    def get_queryset(self):
        queryset = Image.objects.filter(id=self._get_image())
        return queryset
