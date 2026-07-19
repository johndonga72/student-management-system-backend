"""
Database models for the courses application.
"""
from __future__ import annotations
from django.db import models
from apps.departments.models import Department
from apps.core.models import TimeStampedModel
class Course(TimeStampedModel):
    """
    Represents a course offered by a department.
    """
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="courses",
    )
    name = models.CharField(
        max_length=150,
    )
    code = models.CharField(
        max_length=20,
    )
    description = models.TextField(
        blank=True,
    )
    credits = models.PositiveSmallIntegerField()

    is_active = models.BooleanField(
        default=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )
    class Meta:
        db_table = "courses"
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["department", "code"],
                name="unique_course_code_per_department",
            )
        ]
    def __str__(self) -> str:
        """
        Return the string representation of the course.
        """
        return f"{self.code} - {self.name}"