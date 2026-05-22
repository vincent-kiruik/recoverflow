from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=50, choices=[
        ('ADMIN', 'Admin'),
        ('BRANCH_MANAGER', 'Branch Manager'),
        ('RECOVERY_SUPERVISOR', 'Recovery Supervisor'),
        ('COLLECTOR', 'Collector'),
        ('AUDITOR', 'Auditor'),
    ])
    branch = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    supervisor = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"