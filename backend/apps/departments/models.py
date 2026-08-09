"""
Database models for the departments application.
"""
from django.db import models
from apps.core.models import TimeStampedModel
from apps.tenants.models import Tenant
from apps.core.managers import TenantAwareManager

class Department(TimeStampedModel):
    """
    Represents an academic department within the institution.
    """
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        related_name="departments",
        help_text="Tenant that owns this department.",
    )
    name = models.CharField(
        max_length=100,
        help_text="Name of the department within the tenant.",
    )

    code = models.CharField(
        max_length=10,
        help_text="Short code for the department within the tenant.",
    )

    description = models.TextField(
        blank=True,
        help_text="Optional description of the department.",
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Indicates whether the department is active.",
    )

    is_deleted = models.BooleanField(
        default=False,
        help_text="Soft delete flag.",
    )

    objects = TenantAwareManager()

    class Meta:
        """
        Metadata options for the Department model.
        """

        db_table = "departments"

        verbose_name = "Department"

        verbose_name_plural = "Departments"

        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["tenant", "name"],
                name="unique_department_name_per_tenant",
            ),
            models.UniqueConstraint(
                fields=["tenant", "code"],
                name="unique_department_code_per_tenant",
            ),
        ]

    def __str__(self) -> str:
        """
        Return a readable string representation of the department.
        """

        return f"{self.code} - {self.name}"