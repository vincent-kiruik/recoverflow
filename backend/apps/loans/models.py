from django.db import models
from uuid import uuid4
from apps.borrowers.models import Borrower
from apps.groups.models import Group

class Loan(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('OVERDUE', 'Overdue'),
        ('PAID', 'Paid'),
        ('DEFAULTED', 'Defaulted'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    loan_number = models.CharField(max_length=50, unique=True)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE, related_name='loans')
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.SET_NULL, related_name='loans')
    principal_amount = models.DecimalField(max_digits=15, decimal_places=2)
    outstanding_balance = models.DecimalField(max_digits=15, decimal_places=2)
    interest_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    penalty_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    days_overdue = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    disbursement_date = models.DateField()
    last_repayment_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-disbursement_date']

    def __str__(self):
        return f"Loan {self.loan_number} - {self.borrower.full_name}"