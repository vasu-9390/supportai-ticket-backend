from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    total_tickets = serializers.SerializerMethodField()
    open_tickets = serializers.SerializerMethodField()
    resolved_tickets = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = (
            'id', 'name', 'email', 'phone', 'company', 'tier', 
            'profile_image', 'avatar', 'created_at', 'updated_at',
            'total_tickets', 'open_tickets', 'resolved_tickets'
        )

    def get_avatar(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80"

    def get_total_tickets(self, obj):
        return getattr(obj, 'tickets', None) and obj.tickets.count() or 0

    def get_open_tickets(self, obj):
        return getattr(obj, 'tickets', None) and obj.tickets.filter(status='OPEN').count() or 0

    def get_resolved_tickets(self, obj):
        return getattr(obj, 'tickets', None) and obj.tickets.filter(status='RESOLVED').count() or 0
