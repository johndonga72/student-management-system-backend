# Create your models here.
"""
Database models for the Accounts application.

This module defines the custom user model used throughout the
Student Management System.
"""
from __future__ import annotations
from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
class UserRole(models.TextChoices):
    """
    Enumeration of supported user roles.
    """
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    ADMIN = "ADMIN", "Administrator"
    TEACHER = "TEACHER", "Teacher"
    STUDENT = "STUDENT", "Student"
class CustomUser(AbstractUser):
    """
    Custom user model for the Student Management System.

    Authentication is performed using the email address instead
    of the default username field.
    """
    username = None
    email = models.EmailField(
        unique=True,
        help_text="Unique email address used for authentication.",
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        help_text="User contact number.",
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.STUDENT,
        help_text="Role assigned to the user.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []
    objects = CustomUserManager()
    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]
    def __str__(self) -> str:
        """
        Return the string representation of the user.
        """
        return self.email
    