from django.db import models

class Customer(models.Model):
    TIER_CHOICES = (
        ('Enterprise', 'Enterprise'),
        ('Pro', 'Pro'),
        ('Starter', 'Starter'),
    )

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    company = models.CharField(max_length=255, default='Acme Corp')
    tier = models.CharField(max_length=50, choices=TIER_CHOICES, default='Pro')
    profile_image = models.ImageField(upload_to='customers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.company})"
