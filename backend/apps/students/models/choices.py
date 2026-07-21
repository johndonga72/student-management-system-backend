"""
Choice definitions for the Student module.
"""
from django.db import models
class StudentStatus(models.TextChoices):
    """
    Available statuses for a student.
    """
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    SUSPENDED = "SUSPENDED", "Suspended"
    GRADUATED = "GRADUATED", "Graduated"
class Gender(models.TextChoices):
    """
    Available gender options for a student.
    """
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    OTHER = "OTHER", "Other"