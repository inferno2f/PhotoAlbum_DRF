from django.shortcuts import render
from .models import Image
from rest_framework import viewsets, mixins


class AlbumViewSet(mixins.ListModelMixin, mixins.CreateModelMixin):
    query = Image.objects.all()


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
