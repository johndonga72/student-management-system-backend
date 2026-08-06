"""
Tenant model.

This module defines the Tenant model, which represents an
independent educational organization within the Student ERP
platform.

Every tenant owns its own users, departments, courses,
subjects, attendance, examinations, and results.
"""
from django.db import models
from apps.core.models import TimeStampedModel
from .choices import TenantStatus
class Tenant(TimeStampedModel):
    """
    Represents an educational organization in the platform.
    Each tenant is completely isolated from other tenants and owns
    its academic and administrative data.
    """
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="Official name of the educational organization.",
    )

    code = models.SlugField(
        max_length=50,
        unique=True,
        help_text="Unique tenant code used for tenant identification.",
    )

    email = models.EmailField(
        unique=True,
        help_text="Official email address of the organization.",
    )

    phone_number = models.CharField(
        max_length=15,
        help_text="Official contact number of the organization.",
    )

    address = models.TextField(
        blank=True,
        help_text="Organization address.",
    )

    status = models.CharField(
        max_length=20,
        choices=TenantStatus.choices,
        default=TenantStatus.ACTIVE,
    )

    is_deleted = models.BooleanField(
        default=False,
        help_text="Soft delete flag.",
    )

    class Meta:
        db_table = "tenants"
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """
        Return the tenant name.
        """
        return self.name