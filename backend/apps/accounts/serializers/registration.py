"""
Serializers responsible for user registration.

This module contains serializers used to validate and create
new student user accounts.
"""
from __future__ import annotations
from typing import Any
from rest_framework import serializers
from apps.accounts.models import CustomUser, UserRole
class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for student self-registration.
    This serializer allows public users to create only
    student accounts. The user role is assigned automatically
    by the backend.
    """
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "password",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }
    def create(self, validated_data: dict[str, Any]) -> CustomUser:
        """
        Create and return a new student user.
        Args:
            validated_data: Validated serializer data.
        Returns:
            CustomUser: Newly created student user.
        """
        return CustomUser.objects.create_user(
            role=UserRole.STUDENT,
            **validated_data,
        )
