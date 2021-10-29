from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Image, User


class RegisterSerializer(serializers.ModelSerializer):

    def validate_password(self, value: str) -> str:
        """ Returns hashed password """
        return make_password(value, hasher='default')

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

        def create(self, validated_data):
            user = User.objects.create_user(
                validated_data['username'],
                password=validated_data['password'])
            return user


class UserSerializer(serializers.ModelSerializer):
    """ User model serializer """
    class Meta:
        model = User
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False)
    image = serializers.ImageField()

    def validate_image(self, image):
        """Ensuring that the file size doesn't exceed 5 Mb"""
        MAX_FILE_SIZE = 5000000
        if image.size > MAX_FILE_SIZE:
            raise ValidationError('Image size can\'t exceed 5 Mb.')

    class Meta:
        fields = '__all__'
        model = Image
        read_only_fields = ('date_added',)
