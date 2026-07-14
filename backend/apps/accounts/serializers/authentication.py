"""
Serializers responsible for user authentication.

This module contains serializers used during the
authentication process.
"""
from __future__ import annotations
from rest_framework import serializers
class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )