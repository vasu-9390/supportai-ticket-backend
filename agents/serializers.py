from rest_framework import serializers
from .models import Agent
from users.serializers import UserSerializer

class AgentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    avatar = serializers.SerializerMethodField()
    assignedTickets = serializers.IntegerField(source='total_assigned', read_only=True)
    resolvedTickets = serializers.IntegerField(source='total_resolved', read_only=True)
    avgResponseTime = serializers.CharField(source='average_response_time', read_only=True)
    avgResolutionTime = serializers.CharField(source='average_resolution_time', read_only=True)
    rating = serializers.FloatField(source='customer_rating', read_only=True)

    class Meta:
        model = Agent
        fields = (
            'id', 'name', 'email', 'avatar', 'role', 'skills', 'status',
            'workload', 'assignedTickets', 'resolvedTickets', 
            'avgResponseTime', 'avgResolutionTime', 'rating', 'created_at'
        )

    def get_avatar(self, obj):
        if obj.user and obj.user.profile_image:
            return obj.user.profile_image.url
        return "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80"
