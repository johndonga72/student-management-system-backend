"""
Subject model.

This module defines the Subject model used to manage
academic subjects offered under a course.
"""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from apps.courses.models import Course
from apps.core.models import TimeStampedModel
class Subject(TimeStampedModel):
    """
    Represents an academic subject offered under a course.
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="subjects",
        verbose_name="Course",
    )
    subject_name = models.CharField(
        max_length=250,
        verbose_name="Subject Name",
    )
    subject_code = models.CharField(
        max_length=20,
        verbose_name="Subject Code",
    )
    semester = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(8),
        ],
        verbose_name="Semester",
    )
    credits = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(6),
        ],
        verbose_name="Credits",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active Status",
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name="Deleted Status",
    )
    class Meta:
        """
        Metadata options for the Subject model.
        """

        db_table = "subjects"

        verbose_name = "Subject"

        verbose_name_plural = "Subjects"

        ordering = [
            "semester",
            "subject_name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "course",
                    "subject_name",
                ],
                name="unique_subject_name_per_course",
            ),
            models.UniqueConstraint(
                fields=[
                    "course",
                    "subject_code",
                ],
                name="unique_subject_code_per_course",
            ),
        ]
    def __str__(self) -> str:
        """
        Return the string representation of the subject.
        """
        return (
            f"{self.subject_name} "
            f"({self.course.name})"
        )