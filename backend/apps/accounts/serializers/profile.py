"""
Serializers responsible for user profile operations.

This module contains serializers used to represent and manage
user profile information.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.accounts.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for representing authenticated user information.
    """

    tenant_name = serializers.CharField(
        source="tenant.name",
        read_only=True,
    )

    tenant_code = serializers.CharField(
        source="tenant.code",
        read_only=True,
    )
    class Meta:
        """
        Metadata configuration for the UserSerializer.
        """

        model = CustomUser

        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "tenant_name",
            "tenant_code",
        )

        read_only_fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "tenant_name",
            "tenant_code",
        )