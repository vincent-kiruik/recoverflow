from django.db import models
from uuid import uuid4
from apps.loans.models import Loan
from apps.accounts.models import User

class RecoveryCase(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('CONTACT_ATTEMPT', 'Contact Attempt'),
        ('PROMISE_TO_PAY', 'Promise to Pay'),
        ('PARTIAL_RECOVERY', 'Partial Recovery'),
        ('FIELD_VISIT', 'Field Visit'),
        ('ESCALATED', 'Escalated'),
        ('LEGAL_REVIEW', 'Legal Review'),
        ('CLOSED', 'Closed'),
    ]

    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    case_number = models.CharField(max_length=50, unique=True)
    loan = models.OneToOneField(Loan, on_delete=models.CASCADE, related_name='recovery_case')
    assigned_collector = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_cases')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='NEW')
    escalation_level = models.IntegerField(default=0)
    next_action_date = models.DateField(null=True, blank=True)
    promise_to_pay_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    promise_to_pay_date = models.DateField(null=True, blank=True)
    total_collected = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    recovery_percentage = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-opened_at']

    def __str__(self):
        return f"Case {self.case_number} - {self.loan.loan_number}"