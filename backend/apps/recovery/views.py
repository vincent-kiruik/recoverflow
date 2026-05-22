from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import RecoveryCase
from .serializers import RecoveryCaseSerializer

class RecoveryCaseViewSet(viewsets.ModelViewSet):
    queryset = RecoveryCase.objects.all()
    serializer_class = RecoveryCaseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'assigned_collector']
    search_fields = ['case_number', 'loan__loan_number', 'loan__borrower__full_name']
    ordering_fields = ['opened_at', 'next_action_date', 'days_overdue']