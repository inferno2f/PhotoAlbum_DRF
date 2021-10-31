from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from ..models import User, Image


User = get_user_model()


class URLTest(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='John', password='Doe')
        cls.image = Image.objects.create(
            author=cls.user,
            description='no image here',
        )
        cls.private_endpoints = ['/api/v1/album/', '/api/v1/album/image/1/']

    def setUp(self) -> None:
        self.guest_client = APIClient()
        self.user = User.objects.get(username='John')
        self.authorized_client = APIClient()
        self.authorized_client.force_login(self.user)

    def test_unauthorized_users_401(self):
        for address in self.private_endpoints:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code,
                                 status.HTTP_401_UNAUTHORIZED)

    def test_new_user_signup(self):
        url = '/api/v1/register/'
        response = self.guest_client.post(
            url, {'username': 'new_user', 'password': 'password'},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_jwt_token(self):
        url = '/api/v1/token/create/'
        response = self.authorized_client.post(
            url, {'username': 'John', 'password': 'Doe'}, format='json')
        self.assertTrue('access' in response.data, 'No token was found')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
