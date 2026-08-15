from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from customers.models import Customer
from tickets.models import Ticket

User = get_user_model()

class TicketTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="agent.test@supportai.com",
            name="Agent Test",
            password="password123",
            role="Agent"
        )
        self.client.force_authenticate(user=self.user)
        self.customer = Customer.objects.create(
            name="John Smith",
            email="john.smith@acme.corp"
        )

    def test_create_ticket_with_ai_routing(self):
        payload = {
            "customerName": "John Smith",
            "customerEmail": "john.smith@acme.corp",
            "subject": "Payment failed during checkout code ERR_5002",
            "description": "Card debited twice but invoice unpaid",
            "category": "Auto Detect",
            "priority": "Auto Detect"
        }
        response = self.client.post('/api/tickets/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['category'], 'PAYMENT')

    def test_list_tickets(self):
        Ticket.objects.create(
            ticket_number="TK-1001",
            customer=self.customer,
            subject="Test subject",
            description="Test desc",
            category="TECHNICAL",
            priority="HIGH",
            status="OPEN"
        )
        response = self.client.get('/api/tickets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
