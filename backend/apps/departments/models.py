"""
Database models for the departments application.
"""
from django.db import models
from apps.core.models import TimeStampedModel
class Department(TimeStampedModel):
    """
    Represents an academic department within the institution.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique name of the department.",
    )
    code = models.CharField(
        max_length=10,
        unique=True,
        help_text="Unique short code for the department.",
    )
    description = models.TextField(
        blank=True,
        help_text="Optional description of the department.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates whether the department is active.",
    )
    class Meta:
        """
        Metadata options for the Department model.
        """
        db_table = "departments"
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ["name"]
    def __str__(self) -> str:
        """
        Return a readable string representation of the department.
        """
        return f"{self.code} - {self.name}"