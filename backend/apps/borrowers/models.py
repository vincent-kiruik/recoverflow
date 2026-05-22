from django.db import models
from uuid import uuid4
from apps.groups.models import Group

class Borrower(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    client_code = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=255)
    national_id = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    risk_level = models.CharField(max_length=20, choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')], default='MEDIUM')
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.SET_NULL, related_name='members')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return f"{self.full_name} ({self.client_code})"