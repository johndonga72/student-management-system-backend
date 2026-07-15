"""
Serializers responsible for user authentication.

This module contains serializers used during the
authentication process.
"""
from __future__ import annotations
from rest_framework import serializers
from apps.accounts.serializers.profile import UserSerializer
class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )
class TokenResponseSerializer(serializers.Serializer):
    """
    Serializer representing a successful authentication response.

    This serializer is used to return JWT tokens along with
    authenticated user information after a successful login.
    """

    access = serializers.CharField(
        read_only=True,
    )

    refresh = serializers.CharField(
        read_only=True,
    )

    user = UserSerializer(
        read_only=True,
    )