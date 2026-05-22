from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    full_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=30, choices=[
        ('ADMIN', 'System Admin'),
        ('BRANCH_MANAGER', 'Branch Manager'),
        ('RECOVERY_SUPERVISOR', 'Recovery Supervisor'),
        ('LOAN_CLERK', 'Loan Clerk'),
        ('AUDITOR', 'Auditor'),
        ('ANALYST', 'Analyst'),
    ], default='LOAN_CLERK')
    branch = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    supervisor = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subordinates')

    # Fix for clashes with default auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Changed related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  # Changed related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name']
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.full_name} - {self.role}"