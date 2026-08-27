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
from apps.tenants.models import Tenant
from apps.tenants.models.choices import TenantStatus
class AuthenticationService:
    """
    Service responsible for authenticating users
    and generating JWT tokens.
    """

    @staticmethod
    def authenticate_user(
        *,
        email: str,
        password: str,
        tenant: Tenant,
    ) -> CustomUser:
        """
        Authenticate a user within the specified tenant.

        Args:
            email:
                User email address.

            password:
                User password.

            tenant:
                Current tenant obtained from the tenant
                middleware.

        Returns:
            CustomUser:
                Authenticated user.

        Raises:
            AuthenticationFailed:
                If authentication fails or the user does
                not belong to the current tenant.
        """

        if tenant.status != TenantStatus.ACTIVE:
            raise AuthenticationFailed(
                "Tenant is inactive."
            )

        if tenant.is_deleted:
            raise AuthenticationFailed(
                "Tenant not found."
            )

        user = authenticate(
            email=email,
            password=password,
        )

        if user is None:
            raise AuthenticationFailed(
                "Invalid email or password."
            )

        if not user.is_active:
            raise AuthenticationFailed(
                "User account is inactive."
            )

        if user.tenant_id != tenant.id:
            raise AuthenticationFailed(
                "User does not belong to this tenant."
            )

        return user

    @staticmethod
    def generate_tokens(
        user: CustomUser,
    ) -> dict[str, Any]:
        """
        Generate JWT access and refresh tokens.

        Args:
            user:
                Authenticated user.

        Returns:
            dict[str, Any]:
                Access token, refresh token, and
                authenticated user.
        """

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": user,
        }