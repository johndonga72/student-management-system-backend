"""
Business services responsible for user registration.
This module contains the business logic required to register
new student accounts in the Student Management System.
"""
from __future__ import annotations
from typing import Any
from apps.accounts.models import CustomUser, UserRole
class RegistrationService:
    """
    Service responsible for registering new student accounts.
    """
    @staticmethod
    def register_user(validated_data: dict[str, Any]) -> CustomUser:
        """
        Register and return a new student user.
        Args:
            validated_data: Validated registration data.
        Returns:
            CustomUser: Newly created student account.
        """
        return CustomUser.objects.create_user(
            role=UserRole.STUDENT,
            **validated_data,
        )
