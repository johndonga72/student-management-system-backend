
"""
Serializers for department-related operations.
"""

from rest_framework import serializers

from apps.departments.models import Department


class TenantAwareSerializerMixin:
    """
    Provides access to the current tenant from serializer context.
    """

    def get_tenant(self):
        """
        Return the current tenant from serializer context.
        """

        tenant = self.context.get("tenant")

        if tenant is None:
            raise serializers.ValidationError(
                "Tenant context is required."
            )

        return tenant


class DepartmentCreateSerializer(
    TenantAwareSerializerMixin,
    serializers.ModelSerializer,
):
    """
    Serializer for creating a new department.
    """

    class Meta:
        """
        Serializer configuration.
        """

        model = Department

        fields = (
            "name",
            "code",
            "description",
        )

    def validate_name(self, value: str) -> str:
        """
        Validate that the department name is unique
        within the current tenant.
        """

        value = value.strip()

        tenant = self.get_tenant()

        queryset = Department.objects.for_tenant(
            tenant
        ).filter(
            name__iexact=value,
        )

        if queryset.exists():
            raise serializers.ValidationError(
                "A department with this name already exists."
            )

        return value

    def validate_code(self, value: str) -> str:
        """
        Validate that the department code is unique
        within the current tenant.
        """

        value = value.strip().upper()

        tenant = self.get_tenant()

        queryset = Department.objects.for_tenant(
            tenant
        ).filter(
            code__iexact=value,
        )

        if queryset.exists():
            raise serializers.ValidationError(
                "A department with this code already exists."
            )

        return value


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving department details.
    """

    class Meta:
        """
        Serializer configuration.
        """

        model = Department

        fields = (
            "id",
            "name",
            "code",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields


class DepartmentUpdateSerializer(
    TenantAwareSerializerMixin,
    serializers.ModelSerializer,
):
    """
    Serializer for updating department information.
    """

    class Meta:
        """
        Serializer configuration.
        """

        model = Department

        fields = (
            "name",
            "code",
            "description",
            "is_active",
        )

    def validate_name(self, value: str) -> str:
        """
        Validate that the department name remains unique
        within the current tenant.
        """

        value = value.strip()

        tenant = self.get_tenant()

        queryset = Department.objects.for_tenant(
            tenant
        ).filter(
            name__iexact=value,
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "A department with this name already exists."
            )

        return value

    def validate_code(self, value: str) -> str:
        """
        Validate that the department code remains unique
        within the current tenant.
        """

        value = value.strip().upper()

        tenant = self.get_tenant()

        queryset = Department.objects.for_tenant(
            tenant
        ).filter(
            code__iexact=value,
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError(
                "A department with this code already exists."
            )

        return value


class DepartmentStatusSerializer(serializers.Serializer):
    """
    Serializer for changing the status of a department.
    """

    is_active = serializers.BooleanField()

    def validate_is_active(self, value):
        """
        Validate the department status.
        """

        if not isinstance(value, bool):
            raise serializers.ValidationError(
                "is_active must be either true or false."
            )
            
        return value
