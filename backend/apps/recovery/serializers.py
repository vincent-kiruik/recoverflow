from rest_framework import serializers
from .models import RecoveryCase
from apps.loans.serializers import LoanSerializer
from apps.accounts.serializers import UserSerializer

class RecoveryCaseSerializer(serializers.ModelSerializer):
    loan_details = LoanSerializer(source='loan', read_only=True)
    assigned_collector_name = serializers.CharField(source='assigned_collector.full_name', read_only=True)
    recovery_percentage = serializers.SerializerMethodField()

    class Meta:
        model = RecoveryCase
        fields = [
            'id', 'case_number', 'loan', 'loan_details', 'assigned_collector',
            'assigned_collector_name', 'priority', 'status', 'escalation_level',
            'next_action_date', 'promise_to_pay_amount', 'promise_to_pay_date',
            'total_collected', 'recovery_percentage', 'opened_at', 'closed_at'
        ]

    def get_recovery_percentage(self, obj):
        return obj.recovery_percentage