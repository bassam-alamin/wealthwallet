from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from knox.models import AuthToken


User = get_user_model()


class UserViewSetTest(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(
            first_name='admin', last_name="last_name", email='admin@test.com', password='admin123', is_staff=True,
            is_admin=True
        )
        self.user = User.objects.create_user(
            first_name='user', last_name="last_name", email='user@test.com', password='user123'
        )
        self.token = AuthToken.objects.create(user=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token[1]))

    def test_list_users(self):
        url = reverse('auth_users_management')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_retrieve_user(self):
        url = reverse('auth_users_cms', kwargs={'id': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_list_users_permission_denied(self):
        self.client.credentials()
        url = reverse('auth_users_management')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
