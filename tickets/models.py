from django.db import models
from django.conf import settings
from customers.models import Customer
from agents.models import Agent

class Ticket(models.Model):
    CATEGORY_CHOICES = (
        ('TECHNICAL', 'Technical'),
        ('PAYMENT', 'Payment'),
        ('ACCOUNT', 'Account'),
        ('DELIVERY', 'Delivery'),
        ('REFUND', 'Refund'),
        ('OTHER', 'Other'),
    )

    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    )

    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('WAITING', 'Waiting'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    )

    SENTIMENT_CHOICES = (
        ('POSITIVE', 'Positive'),
        ('NEUTRAL', 'Neutral'),
        ('NEGATIVE', 'Negative'),
    )

    ticket_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='TECHNICAL')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='OPEN')
    sentiment = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default='NEUTRAL')
    sentiment_score = models.FloatField(default=0.0)
    ai_confidence = models.FloatField(default=0.90)
    required_skills = models.JSONField(default=list)
    assigned_agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    ai_suggested_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.ticket_number} - {self.subject} ({self.status})"

class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.ticket.ticket_number}: {self.file_name}"

class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.ticket.ticket_number} by {self.user.name}"
