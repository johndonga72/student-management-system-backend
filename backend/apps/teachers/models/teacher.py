"""
Teacher model.
This module defines the Teacher model, which stores
professional information for approved teachers.
"""
from django.db import models
from apps.accounts.models import CustomUser
from apps.departments.models import Department
from apps.subjects.models import Subject
from apps.teachers.models.choices import TeacherDesignation
from apps.core.models import TimeStampedModel
class Teacher(TimeStampedModel):
    """
    Represents a teacher profile.

    This model stores professional information about
    teachers after administrator approval.
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
        help_text="Associated user account.",
    )
    employee_id = models.CharField(
        max_length=20,
        unique=True,
        help_text="Unique employee identifier.",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="teachers",
        help_text="Department assigned to the teacher.",
    )
    subjects = models.ManyToManyField(
        Subject,
        related_name="teachers",
        blank=True,
        help_text="Subjects taught by the teacher.",
    )
    designation = models.CharField(
        max_length=50,
        choices=TeacherDesignation.choices,
        help_text="Teacher designation.",
    )
    qualification = models.CharField(
        max_length=150,
        help_text="Highest qualification.",
    )
    specialization = models.CharField(
        max_length=150,
        blank=True,
        help_text="Area of specialization.",
    )
    experience_years = models.PositiveSmallIntegerField(
        default=0,
        help_text="Total teaching experience in years.",
    )
    joining_date = models.DateField(
        help_text="Date of joining the institution.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates whether the teacher is active.",
    )
    is_deleted = models.BooleanField(
        default=False,
        help_text="Soft delete flag.",
    )
    class Meta:
        db_table = "teachers"
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
        ordering = [
            "employee_id",
        ]
    def __str__(self) -> str:
        """
        Return the teacher representation.
        """
        return f"{self.employee_id} - {self.user.get_full_name()}"