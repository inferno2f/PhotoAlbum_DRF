from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import Image, User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')

        def create(self, validated_data):
            user = User.objects.create_user(
                validated_data['username'],
                password=validated_data['password'])
            return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate_password(self, value: str) -> str:
        """
        Hashing password
        """
        return make_password(value)


class ImageSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False)

    class Meta:
        fields = '__all__'
        model = Image
        read_only_fields = ('date_added',)
