from django.db import models
from apps.core.models import TimeStampedModel
from apps.core.managers import TenantAwareManager
from apps.tenants.models import Tenant
from apps.subjects.models import Subject
from apps.teachers.models import Teacher
from .choices import (
    ExamType,
    Semester,
    ExaminationStatus,
)
class Examination(TimeStampedModel):
    """
    Stores examination details for a subject.
    """
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="examinations",
        help_text="Tenant that owns this examination.",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="examinations",
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        related_name="examinations",
    )
    exam_type = models.CharField(
        max_length=20,
        choices=ExamType.choices,
    )
    semester = models.CharField(
        max_length=20,
        choices=Semester.choices,
    )
    academic_year = models.CharField(
        max_length=20,
    )
    exam_date = models.DateField()
    maximum_marks = models.PositiveIntegerField()
    passing_marks = models.PositiveIntegerField()
    instructions = models.TextField(
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=10,
        choices=ExaminationStatus.choices,
        default=ExaminationStatus.ACTIVE,
    )

    is_deleted = models.BooleanField(
        default=False,
    )
    objects = TenantAwareManager()
    class Meta:
        db_table = "examinations"
        ordering = [
            "-exam_date",
        ]
        verbose_name = "Examination"
        verbose_name_plural = "Examinations"
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "tenant",
                    "subject",
                    "exam_type",
                    "semester",
                    "academic_year",
                ],
                name=(
                    "unique_tenant_subject_exam_"
                    "semester_year"
                ),
            ),
        ]
    def __str__(self):
        return (
            f"{self.subject.subject_name} - "
            f"{self.get_exam_type_display()} "
            f"({self.academic_year})"
        )