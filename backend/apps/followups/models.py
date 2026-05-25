from django.db import models
from uuid import uuid4
from apps.recovery.models import RecoveryCase
from apps.accounts.models import User

class FollowUpAction(models.Model):
    ACTION_TYPES = [
        ('PHONE_CALL', 'Phone Call'),
        ('SMS', 'SMS'),
        ('WHATSAPP', 'WhatsApp'),
        ('GROUP_MEETING', 'Group Meeting'),
        ('FIELD_VISIT', 'Field Visit'),
        ('DEMAND_LETTER', 'Demand Letter'),
        ('PROMISE_TO_PAY', 'Promise to Pay'),
        ('ESCALATION', 'Escalation'),
        ('LEGAL_ACTION', 'Legal Action'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    recovery_case = models.ForeignKey(RecoveryCase, on_delete=models.CASCADE, related_name='follow_ups')
    officer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='follow_ups')
    action_type = models.CharField(max_length=30, choices=ACTION_TYPES)
    notes = models.TextField()
    result = models.TextField(blank=True)
    promise_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    promise_date = models.DateField(null=True, blank=True)
    next_action_date = models.DateField(null=True, blank=True)
    gps_latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    gps_longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    attachment = models.FileField(upload_to='followups/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Follow-up Action"
        verbose_name_plural = "Follow-up Actions"

    def __str__(self):
        return f"{self.get_action_type_display()} - {self.recovery_case.case_number}"