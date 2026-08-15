from django.db import models
from django.conf import settings

class Agent(models.Model):
    STATUS_CHOICES = (
        ('ONLINE', 'Online'),
        ('OFFLINE', 'Offline'),
        ('BUSY', 'Busy'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agent_profile')
    role = models.CharField(max_length=100, default='Support Engineer')
    skills = models.JSONField(default=list, help_text="List of skills e.g. ['Django', 'Python', 'REST API']")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ONLINE')
    workload = models.IntegerField(default=50, help_text="Workload percentage 0-100%")
    total_assigned = models.IntegerField(default=0)
    total_resolved = models.IntegerField(default=0)
    average_response_time = models.CharField(max_length=50, default="12 mins")
    average_resolution_time = models.CharField(max_length=50, default="1.8 hours")
    customer_rating = models.FloatField(default=4.8)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} ({self.role}) - {self.status}"
