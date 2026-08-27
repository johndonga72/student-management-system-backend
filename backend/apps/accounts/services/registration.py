"""
Business services responsible for user registration.

This module contains the business logic required to register
new student accounts in the Student Management System.
"""

from __future__ import annotations

from typing import Any

from rest_framework.exceptions import ValidationError

from apps.accounts.models import CustomUser, UserRole
from apps.tenants.models import Tenant
from apps.tenants.models.choices import TenantStatus


class RegistrationService:
    """
    Service responsible for registering new student accounts.
    """

    @staticmethod
    def register_user(
        *,
        tenant: Tenant,
        validated_data: dict[str, Any],
    ) -> CustomUser:
        """
        Register a new student account within the specified tenant.

        Args:
            tenant:
                Current tenant obtained from the tenant middleware.

            validated_data:
                Validated registration data.

        Returns:
            CustomUser:
                Newly created student account.

        Raises:
            ValidationError:
                If the tenant is inactive or deleted.
        """

        if tenant.is_deleted:
            raise ValidationError(
                "Tenant not found."
            )

        if tenant.status != TenantStatus.ACTIVE:
            raise ValidationError(
                "Tenant is inactive."
            )

        return CustomUser.objects.create_user(
            tenant=tenant,
            role=UserRole.STUDENT,
            **validated_data,
        )