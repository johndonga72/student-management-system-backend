"""
Attendance model.

This module defines the attendance model used
to manage student attendance records.
"""
from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel
from apps.students.models import Student
from apps.subjects.models import Subject
from apps.teachers.models import Teacher
from .choices import AttendanceStatus
class Attendance(TimeStampedModel):
    """
    Represents a student's attendance record
    for a subject on a specific date.
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name="attendance_records",
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        related_name="attendance_records",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="attendance_records",
    )
    attendance_date = models.DateField(
        default=timezone.localdate,
    )
    status = models.CharField(
        max_length=20,
        choices=AttendanceStatus.choices,
        default=AttendanceStatus.PRESENT,
    )
    remarks = models.TextField(
        blank=True,
    )
    class Meta:
        db_table = "attendance"

        verbose_name = "Attendance"

        verbose_name_plural = "Attendance"

        ordering = [
            "-attendance_date",
            "student",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "subject",
                    "attendance_date",
                ],
                name="unique_student_subject_attendance",
            ),
        ]
    def __str__(self) -> str:
        """
        Return the string representation.
        """
        return (
            f"{self.student} - "
            f"{self.subject} - "
            f"{self.attendance_date}"
        )