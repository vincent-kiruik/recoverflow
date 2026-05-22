from django.db import models
from uuid import uuid4

class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    group_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    region = models.CharField(max_length=100)
    chairperson = models.CharField(max_length=255)
    active_members = models.PositiveIntegerField(default=0)
    total_arrears = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    recovery_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0)  # percentage
    risk_level = models.CharField(max_length=20, choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], default='MEDIUM')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.group_code})"