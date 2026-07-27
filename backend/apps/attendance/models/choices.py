"""
Attendance model choices.

This module defines enumerations used by
the attendance module.
"""
from django.db import models
class AttendanceStatus(models.TextChoices):
    """
    Attendance status choices.
    """
    PRESENT = (
        "PRESENT",
        "Present",
    )
    ABSENT = (
        "ABSENT",
        "Absent",
    )
    LATE = (
        "LATE",
        "Late",
    )
    LEAVE = (
        "LEAVE",
        "Leave",
    )