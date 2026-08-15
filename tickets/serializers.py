from rest_framework import serializers
from .models import Ticket, TicketAttachment, TicketComment

class TicketAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketAttachment
        fields = ('id', 'ticket', 'file', 'file_name', 'uploaded_at')

class TicketCommentSerializer(serializers.ModelSerializer):
    senderType = serializers.SerializerMethodField()
    senderName = serializers.CharField(source='user.name', read_only=True)
    senderAvatar = serializers.SerializerMethodField()
    timestamp = serializers.DateTimeField(source='created_at', read_only=True)
    content = serializers.CharField(source='message')

    class Meta:
        model = TicketComment
        fields = ('id', 'senderType', 'senderName', 'senderAvatar', 'timestamp', 'content')

    def get_senderType(self, obj):
        if obj.user.role in ['Admin', 'Agent']:
            return 'agent'
        return 'customer'

    def get_senderAvatar(self, obj):
        if obj.user.profile_image:
            return obj.user.profile_image.url
        if obj.user.role in ['Admin', 'Agent']:
            return "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80"
        return "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80"

class TicketSerializer(serializers.ModelSerializer):
    # Frontend aliases
    id = serializers.CharField(source='ticket_number', read_only=True)
    customerId = serializers.IntegerField(source='customer.id', read_only=True)
    customerName = serializers.CharField(source='customer.name', read_only=True)
    customerEmail = serializers.CharField(source='customer.email', read_only=True)
    customerAvatar = serializers.SerializerMethodField()
    
    assignedAgentId = serializers.SerializerMethodField()
    assignedAgentName = serializers.SerializerMethodField()
    assignedAgentAvatar = serializers.SerializerMethodField()
    
    created = serializers.DateTimeField(source='created_at', read_only=True)
    updated = serializers.DateTimeField(source='updated_at', read_only=True)
    suggestedResponse = serializers.CharField(source='ai_suggested_response', read_only=True)
    
    aiAnalysis = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = (
            'id', 'ticket_number', 'customerId', 'customerName', 'customerEmail', 'customerAvatar',
            'subject', 'description', 'category', 'priority', 'status', 'sentiment',
            'assignedAgentId', 'assignedAgentName', 'assignedAgentAvatar',
            'created', 'updated', 'aiAnalysis', 'suggestedResponse', 'messages',
            'created_at', 'updated_at'
        )

    def get_customerAvatar(self, obj):
        if obj.customer and obj.customer.profile_image:
            return obj.customer.profile_image.url
        return "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150&auto=format&fit=crop&q=80"

    def get_assignedAgentId(self, obj):
        return str(obj.assigned_agent.id) if obj.assigned_agent else ""

    def get_assignedAgentName(self, obj):
        return obj.assigned_agent.user.name if obj.assigned_agent else "Unassigned"

    def get_assignedAgentAvatar(self, obj):
        if obj.assigned_agent and obj.assigned_agent.user.profile_image:
            return obj.assigned_agent.user.profile_image.url
        return "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80"

    def get_aiAnalysis(self, obj):
        return {
            "category": obj.get_category_display(),
            "categoryConfidence": int(obj.ai_confidence * 100),
            "priority": obj.priority,
            "priorityConfidence": int(obj.ai_confidence * 100),
            "sentiment": obj.get_sentiment_display(),
            "sentimentScore": obj.sentiment_score,
            "requiredSkills": obj.required_skills,
            "recommendedAgent": self.get_assignedAgentName(obj),
            "matchScore": 96,
            "suggestedAction": f"Review {obj.get_category_display().lower()} issue diagnostic protocol."
        }

    def get_messages(self, obj):
        comments = obj.comments.all().order_by('created_at')
        return TicketCommentSerializer(comments, many=True).data
