from django.db.models import fields
from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False)

    class Meta:
        fields = '__all__'
        model = Image