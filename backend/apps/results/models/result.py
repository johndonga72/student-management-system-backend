from django.db import models
from apps.core.models import TimeStampedModel
from apps.students.models import Student
from apps.examinations.models import Examination
from apps.tenants.models import Tenant
from apps.core.managers import TenantAwareManager
from .choices import (
    ResultStatus,
    ResultRecordStatus,
)
class Result(TimeStampedModel):
    """
    Represents a student's result for an examination
    within a specific tenant.
    """
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        related_name="results",
        help_text="Tenant that owns this result.",
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name="results",
    )
    examination = models.ForeignKey(
        Examination,
        on_delete=models.PROTECT,
        related_name="results",
    )
    obtained_marks = models.PositiveIntegerField()
    result_status = models.CharField(
        max_length=10,
        choices=ResultStatus.choices,
    )
    remarks = models.TextField(
        blank=True,
    )
    status = models.CharField(
        max_length=10,
        choices=ResultRecordStatus.choices,
        default=ResultRecordStatus.ACTIVE,
    )
    is_deleted = models.BooleanField(
        default=False,
    )
    objects = TenantAwareManager()
    class Meta:
        db_table = "results"

        ordering = [
            "-created_at",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "tenant",
                    "student",
                    "examination",
                ],
                name="unique_tenant_student_examination_result",
            ),
        ]

        verbose_name = "Result"
        verbose_name_plural = "Results"
    def __str__(self) -> str:
        """
        Return string representation of the result.
        """
        return (
            f"{self.student.user.email} - "
            f"{self.examination.subject.subject_name}"
        )