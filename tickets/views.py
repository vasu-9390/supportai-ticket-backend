from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Ticket, TicketAttachment, TicketComment
from .serializers import TicketSerializer, TicketCommentSerializer, TicketAttachmentSerializer
from customers.models import Customer
from agents.models import Agent

class TicketViewSet(viewsets.ModelViewSet):
    lookup_field = 'ticket_number'
    queryset = Ticket.objects.select_related('customer', 'assigned_agent', 'assigned_agent__user').prefetch_related('comments', 'comments__user').all().order_by('-created_at')
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'category', 'assigned_agent']
    search_fields = ['ticket_number', 'subject', 'description', 'customer__name', 'customer__email']
    ordering_fields = ['created_at', 'updated_at', 'priority', 'status']

    def get_queryset(self):
        qs = super().get_queryset()
        status_param = self.request.query_params.get('status')
        priority_param = self.request.query_params.get('priority')
        category_param = self.request.query_params.get('category')
        agent_param = self.request.query_params.get('agent') or self.request.query_params.get('agentId')

        if status_param and status_param != 'All':
            qs = qs.filter(status__iexact=status_param)
        if priority_param and priority_param != 'All':
            qs = qs.filter(priority__iexact=priority_param)
        if category_param and category_param != 'All':
            qs = qs.filter(category__iexact=category_param)
        if agent_param and agent_param != 'All':
            qs = qs.filter(assigned_agent_id=agent_param)

        return qs

    def create(self, request, *args, **kwargs):
        data = request.data
        subject = data.get('subject', '')
        description = data.get('description', '')
        customer_name = data.get('customerName') or data.get('customer_name') or 'John Smith'
        customer_email = data.get('customerEmail') or data.get('customer_email') or 'john.smith@acme.corp'

        # Get or create customer
        customer, _ = Customer.objects.get_or_create(
            email=customer_email,
            defaults={'name': customer_name}
        )

        ticket_count = Ticket.objects.count() + 1044
        ticket_number = f"TK-{ticket_count}"

        # Trigger AI Analysis service
        from ai_engine.services.ticket_analyzer import analyze_ticket_data
        ai_res = analyze_ticket_data(subject, description)

        category = data.get('category')
        if not category or category == 'Auto Detect':
            category = ai_res['category']

        priority = data.get('priority')
        if not priority or priority == 'Auto Detect':
            priority = ai_res['priority']

        # Find & assign best agent
        from ai_engine.services.agent_matcher import match_and_assign_agent
        assigned_agent = match_and_assign_agent(ai_res['required_skills'])

        ticket = Ticket.objects.create(
            ticket_number=ticket_number,
            customer=customer,
            subject=subject,
            description=description,
            category=category.upper(),
            priority=priority.upper(),
            status='OPEN',
            sentiment=ai_res['sentiment'],
            sentiment_score=ai_res['sentiment_score'],
            ai_confidence=ai_res['confidence'],
            required_skills=ai_res['required_skills'],
            assigned_agent=assigned_agent,
            ai_suggested_response=ai_res['suggested_response']
        )

        # Create initial customer message as TicketComment
        TicketComment.objects.create(
            ticket=ticket,
            user=request.user,
            message=description
        )

        serializer = self.get_serializer(ticket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post'], url_path='comments')
    def comments(self, request, pk=None):
        ticket = self.get_object()
        if request.method == 'GET':
            comments = ticket.comments.all().order_by('created_at')
            serializer = TicketCommentSerializer(comments, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            content = request.data.get('content') or request.data.get('message')
            if not content:
                return Response({'detail': 'Message content is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            comment = TicketComment.objects.create(
                ticket=ticket,
                user=request.user,
                message=content
            )
            ticket.updated_at = timezone.now()
            ticket.save()

            serializer = TicketCommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
