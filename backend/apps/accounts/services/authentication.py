"""
Business services responsible for user authentication.

This module contains the business logic required for
user authentication and JWT token generation.
"""
from __future__ import annotations
from typing import Any
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from apps.accounts.models import CustomUser
class AuthenticationService:
    """
    Service responsible for authenticating users
    and generating JWT tokens.
    """
    @staticmethod
    def authenticate_user(
        email: str,
        password: str,
    ) -> CustomUser:
        """
        Authenticate a user using email and password.
        """
        user = authenticate(
            email=email,
            password=password,
        )
        if user is None:
            raise AuthenticationFailed(
                "Invalid email or password."
            )
        return user
    @staticmethod
    def generate_tokens(
        user: CustomUser,
    ) -> dict[str, Any]:
        """
        Generate JWT access and refresh tokens.
        """
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": user,
        }