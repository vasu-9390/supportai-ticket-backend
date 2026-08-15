from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        payload = {
            "fullName": "Test User",
            "email": "test.user@supportai.com",
            "password": "password123",
            "role": "Agent"
        }
        response = self.client.post('/api/auth/register/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_user_login(self):
        User.objects.create_user(
            email="sarah.test@supportai.com",
            name="Sarah Test",
            password="password123",
            role="Admin"
        )
        payload = {
            "email": "sarah.test@supportai.com",
            "password": "password123"
        }
        response = self.client.post('/api/auth/login/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
