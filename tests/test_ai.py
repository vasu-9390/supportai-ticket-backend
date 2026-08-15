from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AIEngineTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="ai.test@supportai.com",
            name="AI Tester",
            password="password123",
            role="Admin"
        )
        self.client.force_authenticate(user=self.user)

    def test_ai_analyze_ticket_endpoint(self):
        payload = {
            "subject": "Payment timeout error on Stripe checkout",
            "description": "Customer card charged twice but no confirmation email."
        }
        response = self.client.post('/api/ai/analyze-ticket/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['category'], 'PAYMENT')

    def test_ai_check_duplicate_endpoint(self):
        payload = {
            "subject": "Payment timeout error",
            "description": "Card charged twice"
        }
        response = self.client.post('/api/ai/check-duplicate/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('is_duplicate', response.data)
