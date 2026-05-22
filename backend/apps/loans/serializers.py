from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    borrower_name = serializers.CharField(source='borrower.full_name', read_only=True)
    
    class Meta:
        model = Loan
        fields = [
            'id', 'loan_number', 'borrower', 'borrower_name', 'group',
            'principal_amount', 'outstanding_balance', 'interest_amount',
            'penalty_amount', 'days_overdue', 'status', 'disbursement_date',
            'last_repayment_date'
        ]