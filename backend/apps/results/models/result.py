from django.db import models
from apps.students.models import Student
from apps.core.models import TimeStampedModel
from apps.examinations.models import Examination
from .choices import (
    ResultStatus,
    ResultRecordStatus,
)
class Result(TimeStampedModel):
    """
    Represents a student's result for an examination.
    """
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
    class Meta:
        db_table = "results"
        ordering = [
            "-created_at",
        ]
        constraints = [
        models.UniqueConstraint(
            fields=[
                "student",
                "examination",
            ],
            name="unique_student_examination_result",
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