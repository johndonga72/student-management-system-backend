"""
Custom managers for the Accounts application.

This module defines the custom manager responsible for creating
regular users and superusers for the CustomUser model.
"""
from __future__ import annotations
from typing import Any
from django.contrib.auth.base_user import BaseUserManager
class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model.

    This manager uses email as the unique identifier instead
    of the default username field.
    """
    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,
    ):
        """
        Create and return a regular user.

        Args:
            email: User's unique email address.
            password: Plain-text password.
            **extra_fields: Additional model fields.

        Returns:
            CustomUser: The newly created user instance.

        Raises:
            ValueError: If the email address is not provided.
        """

        if not email:
            raise ValueError("Email address is required.")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(
        self,
        email: str,
        password: str,
        **extra_fields: Any,
    ):
        """
        Create and return a superuser.

        A superuser has full administrative privileges
        within the Django application.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(
            email=email,
            password=password,
            **extra_fields,
        )