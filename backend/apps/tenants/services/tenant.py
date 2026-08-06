"""
Business services for the Tenant module.

This module contains the business logic for managing tenants.
All tenant-related operations should be implemented through
the service layer to keep API views thin and maintain a clean
architecture.
"""

from django.db import transaction

from apps.tenants.models import Tenant, TenantStatus

from rest_framework.exceptions import ValidationError
from django.db.models import QuerySet

class TenantService:
    """
    Service class for tenant management.

    This service encapsulates all business logic related to
    tenant creation, retrieval, update, status management,
    and soft deletion.
    """
# private helper methods
    @staticmethod
    def _get_tenant(tenant_id: int) -> Tenant:
        """
        Retrieve an active tenant by its unique identifier.

        Args:
            tenant_id (int): Unique identifier of the tenant.

        Returns:
            Tenant: The matching tenant instance.

        Raises:
            Tenant.DoesNotExist: If the tenant does not exist or has been
                soft deleted.
        """
        return Tenant.objects.get(
            pk=tenant_id,
            is_deleted=False,
        )
    @staticmethod
    def _validate_unique_constraints(
        *,
        name: str,
        code: str,
        email: str,
        tenant_id: int | None = None,
    ) -> None:
        """
        Validate tenant unique constraints.

        Args:
            name (str): Tenant name.
            code (str): Tenant code.
            email (str): Tenant email.
            tenant_id (int | None): Existing tenant ID during update.

        Raises:
            ValidationError: If any unique constraint is violated.
        """

        queryset = Tenant.objects.filter(is_deleted=False)

        if tenant_id is not None:
            queryset = queryset.exclude(pk=tenant_id)

        if queryset.filter(name=name).exists():
            raise ValidationError(
                {"name": "Tenant name already exists."}
            )

        if queryset.filter(code=code).exists():
            raise ValidationError(
                {"code": "Tenant code already exists."}
            )

        if queryset.filter(email=email).exists():
            raise ValidationError(
                {"email": "Tenant email already exists."}
            )
    @staticmethod
    def _validate_status_transition(
        current_status: str,
        new_status: str,
    ) -> None:
        """
        Validate tenant status transition.

        Args:
            current_status (str): Current tenant status.
            new_status (str): Requested tenant status.

        Raises:
            ValidationError: If the status transition is not allowed.
        """

        allowed_transitions = {
            TenantStatus.ACTIVE: {
                TenantStatus.INACTIVE,
                TenantStatus.SUSPENDED,
            },
            TenantStatus.INACTIVE: {
                TenantStatus.ACTIVE,
                TenantStatus.SUSPENDED,
            },
            TenantStatus.SUSPENDED: {
                TenantStatus.ACTIVE,
                TenantStatus.INACTIVE,
            },
        }

        if current_status == new_status:
            raise ValidationError(
                {"status": "Tenant is already in the requested status."}
            )

        if new_status not in allowed_transitions.get(current_status, set()):
            raise ValidationError(
                {"status": "Invalid tenant status transition."}
            )
# Bussiness functions
    @staticmethod
    @transaction.atomic
    def create_tenant(validated_data: dict) -> Tenant:
        """
        Create a new tenant.

        Args:
            validated_data (dict): Validated tenant data.

        Returns:
            Tenant: Newly created tenant instance.
        """

        TenantService._validate_unique_constraints(
            name=validated_data["name"],
            code=validated_data["code"],
            email=validated_data["email"],
        )

        tenant = Tenant.objects.create(**validated_data)

        return tenant
    @staticmethod
    def get_tenant_by_id(tenant_id: int) -> Tenant:
        """
        Retrieve a tenant by its unique identifier.

        Args:
            tenant_id (int): Unique identifier of the tenant.

        Returns:
            Tenant: Tenant instance.
        """
        return TenantService._get_tenant(tenant_id)
    @staticmethod
    def list_tenants()-> QuerySet[Tenant]:
        """
        Retrieve all active tenants.

        Returns:
            QuerySet[Tenant]: Queryset containing active tenants.
        """
        return (
            Tenant.objects.filter(is_deleted=False)
            .order_by("-created_at")
        )
    @staticmethod
    @transaction.atomic
    def update_tenant(
        tenant_id: int,
        validated_data: dict,
    ) -> Tenant:
        """
        Update an existing tenant.

        Args:
            tenant_id (int): Unique identifier of the tenant.
            validated_data (dict): Validated tenant data.

        Returns:
            Tenant: Updated tenant instance.
        """

        tenant = TenantService._get_tenant(tenant_id)

        TenantService._validate_unique_constraints(
            name=validated_data.get("name", tenant.name),
            code=tenant.code,
            email=validated_data.get("email", tenant.email),
            tenant_id=tenant.pk,
        )

        for field, value in validated_data.items():
            setattr(tenant, field, value)

        tenant.save(
            update_fields=list(validated_data.keys())
        )
        return tenant
    @staticmethod
    @transaction.atomic
    def change_tenant_status(
        tenant_id: int,
        status: str,
    ) -> Tenant:
        """
        Change the status of an existing tenant.

        Args:
            tenant_id (int): Unique identifier of the tenant.
            status (str): New tenant status.

        Returns:
            Tenant: Updated tenant instance.
        """

        tenant = TenantService._get_tenant(tenant_id)

        TenantService._validate_status_transition(
            current_status=tenant.status,
            new_status=status,
        )

        tenant.status = status

        tenant.save(update_fields=["status","updated_at"])

        return tenant
    
    @staticmethod
    @transaction.atomic
    def delete_tenant(
        tenant_id: int,
    ) -> Tenant:
        """
        Soft delete an existing tenant.

        Args:
            tenant_id (int): Unique identifier of the tenant.

        Returns:
            Tenant: Soft deleted tenant instance.
        """

        tenant = TenantService._get_tenant(tenant_id)

        tenant.is_deleted = True

        tenant.save(update_fields=["is_deleted"])

        return tenant