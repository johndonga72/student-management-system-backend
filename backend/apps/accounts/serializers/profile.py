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

    This serializer is used to return user details in API responses,
    such as the login response and profile endpoints.
    """
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
        )
        read_only_fields = [
        "id",
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "role",
    ]