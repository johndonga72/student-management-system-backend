"""
Choice constants for the Examination model.
"""
from django.db import models
class ExamType(models.TextChoices):
    """
    Supported examination types.
    """
    MID_1 = "MID_1", "Mid-1"
    MID_2 = "MID_2", "Mid-2"
    INTERNAL = "INTERNAL", "Internal"
    PRACTICAL = "PRACTICAL", "Practical"
    SEMESTER = "SEMESTER", "Semester"
    SUPPLEMENTARY = "SUPPLEMENTARY", "Supplementary"
class Semester(models.TextChoices):
    """
    Academic semester choices.
    """
    SEMESTER_1 = "SEMESTER_1", "Semester-I"
    SEMESTER_2 = "SEMESTER_2", "Semester-II"

class ExaminationStatus(models.TextChoices):
    """
    Examination status choices.
    """
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
