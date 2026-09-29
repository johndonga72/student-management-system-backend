"""
Business services for department-related operations.
"""

from apps.departments.models import Department
from apps.core.cache.helpers import get_cache, set_cache
from apps.core.cache.keys import DepartmentCacheKeys
from apps.departments.models import Department
from typing import Any
class DepartmentService:
    """
    Service class containing business logic for department operations.
    """

    @staticmethod
    def create_department(
        tenant,
        validated_data: dict,
    ) -> Department:
        """
        Create a new department for the given tenant.

        Args:
            tenant: Current tenant.
            validated_data: Validated department data.

        Returns:
            Department: The newly created department instance.
        """

        return Department.objects.create(
            tenant=tenant,
            **validated_data,
        )

    @staticmethod
    def list_departments(
        tenant,
    ) -> list[dict[str, Any]]:
        """
        Retrieve active, non-deleted departments for the tenant.

        Uses a tenant-aware cache-aside strategy.

        Args:
            tenant: Current tenant.

        Returns:
            list[dict[str, Any]]: Department data for the tenant.
        """

        cache_key = DepartmentCacheKeys.list(
            tenant_id=tenant.id,
        )

        cached_departments = get_cache(
            cache_key,
        )

        if cached_departments is not None:
            return cached_departments

        departments = (
            Department.objects
            .for_tenant(tenant)
            .filter(
                is_active=True,
                is_deleted=False,
            )
            .order_by("name")
            .values(
                "id",
                "name",
                "code",
                "description",
                "is_active",
                "created_at",
                "updated_at",
            )
        )

        department_data = list(departments)

        set_cache(
            key=cache_key,
            value=department_data,
            timeout=DepartmentService.DEPARTMENT_LIST_CACHE_TIMEOUT,
        )

        return department_data

    @staticmethod
    def get_department_by_id(
        tenant,
        department_id: int,
    ) -> Department:
        """
        Retrieve an active department belonging to
        the given tenant.

        Args:
            tenant: Current tenant.
            department_id: Department primary key.

        Returns:
            Department: Department instance.

        Raises:
            Department.DoesNotExist:
                If the department does not exist
                within the tenant.
        """

        return (
            Department.objects
            .for_tenant(tenant)
            .get(
                id=department_id,
                is_active=True,
                is_deleted=False,
            )
        )

    @staticmethod
    def update_department(
        tenant,
        department_id: int,
        validated_data: dict,
    ) -> Department:
        """
        Update an existing department within the tenant.

        Args:
            tenant: Current tenant.
            department_id: Department primary key.
            validated_data: Validated update data.

        Returns:
            Department: Updated department instance.
        """

        department = DepartmentService.get_department_by_id(
            tenant=tenant,
            department_id=department_id,
        )

        for field, value in validated_data.items():
            setattr(department, field, value)

        department.save()

        return department

    @staticmethod
    def change_department_status(
        tenant,
        department_id: int,
        is_active: bool,
    ) -> Department:
        """
        Activate or deactivate a department within
        the tenant.

        Args:
            tenant: Current tenant.
            department_id: Department primary key.
            is_active: New active status.

        Returns:
            Department: Updated department instance.
        """

        department = DepartmentService.get_department_by_id(
            tenant=tenant,
            department_id=department_id,
        )

        department.is_active = is_active

        department.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        return department

    @staticmethod
    def delete_department(
        tenant,
        department_id: int,
    ) -> None:
        """
        Soft delete a department within the tenant.

        Args:
            tenant: Current tenant.
            department_id: Department primary key.
        """

        department = DepartmentService.get_department_by_id(
            tenant=tenant,
            department_id=department_id,
        )

        department.is_active = False
        department.is_deleted = True

        department.save(
            update_fields=[
                "is_active",
                "is_deleted",
                "updated_at",
            ]
        )