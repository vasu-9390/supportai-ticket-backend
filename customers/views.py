from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def tickets(self, request, pk=None):
        customer = self.get_object()
        from tickets.serializers import TicketSerializer
        tickets = customer.tickets.all().order_by('-created_at')
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)
