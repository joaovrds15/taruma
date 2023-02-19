from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
import json

# Create your tests here.
class LoginTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='username', password='testpass')
        self.url = reverse('login')
    
    def test_valid_login(self):
        data = {'username': 'username', 'password': 'testpass'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_invalid_login(self):
        data = {'username': 'testuser', 'password': 'wrongpass'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('token', response.data)