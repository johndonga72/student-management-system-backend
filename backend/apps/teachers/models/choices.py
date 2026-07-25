"""
Teacher module choices.
This module contains reusable choice classes for
teacher-related models.
"""
from django.db import models
class TeacherDesignation(models.TextChoices):
    """
    Available teacher designations.
    """
    ASSISTANT_PROFESSOR = (
        "ASSISTANT_PROFESSOR",
        "Assistant Professor",
    )
    ASSOCIATE_PROFESSOR = (
        "ASSOCIATE_PROFESSOR",
        "Associate Professor",
    )
    PROFESSOR = (
        "PROFESSOR",
        "Professor",
    )
    HEAD_OF_DEPARTMENT = (
        "HEAD_OF_DEPARTMENT",
        "Head of Department",
    )
    GUEST_FACULTY = (
        "GUEST_FACULTY",
        "Guest Faculty",
    )
    LAB_INSTRUCTOR = (
        "LAB_INSTRUCTOR",
        "Lab Instructor",
    )