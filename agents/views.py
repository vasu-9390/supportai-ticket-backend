from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Agent
from .serializers import AgentSerializer

User = get_user_model()

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.select_related('user').all().order_by('-created_at')
    serializer_class = AgentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        email = request.data.get('email')
        role = request.data.get('role', 'Support Engineer')
        skills = request.data.get('skills', ["Django", "Python", "REST API"])

        if not name or not email:
            return Response({'detail': 'Name and Email are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create User for agent
        user, created = User.objects.get_or_create(
            email=email,
            defaults={'name': name, 'role': 'Agent'}
        )
        if created:
            user.set_password("password123")
            user.save()

        agent, _ = Agent.objects.get_or_create(
            user=user,
            defaults={'role': role, 'skills': skills}
        )
        serializer = self.get_serializer(agent)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def tickets(self, request, pk=None):
        agent = self.get_object()
        from tickets.serializers import TicketSerializer
        tickets = agent.assigned_tickets.all().order_by('-created_at')
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        agent = self.get_object()
        return Response({
            'agent_id': agent.id,
            'agent_name': agent.user.name,
            'total_assigned': agent.total_assigned,
            'total_resolved': agent.total_resolved,
            'average_response_time': agent.average_response_time,
            'average_resolution_time': agent.average_resolution_time,
            'customer_rating': agent.customer_rating,
            'workload': agent.workload,
            'resolution_history': [
                {'month': 'Jan', 'resolved': 42, 'csat': 4.8},
                {'month': 'Feb', 'resolved': 56, 'csat': 4.9},
                {'month': 'Mar', 'resolved': 68, 'csat': 4.9},
                {'month': 'Apr', 'resolved': 74, 'csat': 4.85},
                {'month': 'May', 'resolved': 82, 'csat': 4.95},
                {'month': 'Jun', 'resolved': 90, 'csat': 4.9},
            ]
        })
