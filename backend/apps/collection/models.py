from django.db import models
from uuid import uuid4
from apps.recovery.models import RecoveryCase
from apps.loans.models import Loan
from apps.accounts.models import User

class Collection(models.Model):
    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('MPESA', 'M-Pesa'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('CHEQUE', 'Cheque'),
        ('INTERNAL_OFFSET', 'Internal Offset'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    recovery_case = models.ForeignKey(RecoveryCase, on_delete=models.CASCADE, related_name='collections')
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount_collected = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHODS)
    receipt_number = models.CharField(max_length=100, blank=True)
    collected_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='collections_made')
    verified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='verified_collections')
    collection_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-collection_date']