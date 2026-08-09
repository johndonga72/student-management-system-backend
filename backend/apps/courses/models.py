"""
Database models for the courses application.
"""
from __future__ import annotations
from django.db import models
from apps.core.managers import TenantAwareManager
from apps.core.models import TimeStampedModel
from apps.departments.models import Department
from apps.tenants.models import Tenant
class Course(TimeStampedModel):
    """
    Represents a course offered by a department
    within a tenant.
    """

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        related_name="courses",
        help_text="Tenant that owns this course.",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="courses",
        help_text="Department that offers this course.",
    )

    name = models.CharField(
        max_length=150,
        help_text="Name of the course.",
    )

    code = models.CharField(
        max_length=20,
        help_text="Course code within the department.",
    )

    description = models.TextField(
        blank=True,
        help_text="Optional course description.",
    )

    credits = models.PositiveSmallIntegerField()

    is_active = models.BooleanField(
        default=True,
    )

    is_deleted = models.BooleanField(
        default=False,
    )

    objects = TenantAwareManager()

    class Meta:
        db_table = "courses"
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["department", "code"],
                name="unique_course_code_per_department",
            ),
        ]

    def __str__(self) -> str:
        """
        Return the string representation of the course.
        """
        return f"{self.code} - {self.name}"
