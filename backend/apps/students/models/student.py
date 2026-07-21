"""
Student model.
"""

from django.db import models

from apps.accounts.models import CustomUser
from apps.core.models import TimeStampedModel
from apps.courses.models import Course
from apps.departments.models import Department

from .choices import (
    Gender,
    StudentStatus,
)
class Student(TimeStampedModel):
    """
    Stores academic information for a student.
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )

    student_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="students",
        null=True,
        blank=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="students",
        null=True,
        blank=True,
    )

    semester = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    section = models.CharField(
        max_length=10,
        blank=True,
    )

    date_of_birth = models.DateField()

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
    )

    phone = models.CharField(
        max_length=15,
    )

    address = models.TextField()

    guardian_name = models.CharField(
        max_length=100,
    )

    guardian_phone = models.CharField(
        max_length=15,
    )

    admission_date = models.DateField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=StudentStatus.choices,
        default=StudentStatus.PENDING,
    )
    is_deleted = models.BooleanField(
    default=False,
    )
    class Meta:
        db_table = "students"
        ordering = ["student_number"]
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self) -> str:
        return f"{self.student_number} - {self.user.get_full_name()}"