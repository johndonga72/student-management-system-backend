"""
Serializers for the Tenant module.
"""
from rest_framework import serializers

from apps.tenants.models import Tenant

class BaseTenantSerializer(serializers.ModelSerializer):
    """
    Base serializer for Tenant.

    This serializer contains the common fields shared by all
    tenant serializers and serves as the foundation for
    specialized serializers.
    """

    class Meta:
        model = Tenant
        fields = (
            "id",
            "name",
            "code",
            "email",
            "phone_number",
            "address",
            "status",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )
class TenantCreateSerializer(BaseTenantSerializer):
    """
    Serializer for creating a new tenant.

    Performs input validation before delegating tenant creation
    to the service layer.
    """

    class Meta(BaseTenantSerializer.Meta):
        read_only_fields = (
            "id",
            "status",
            "created_at",
            "updated_at",
        )

    def validate_code(self, value: str) -> str:
        """
        Validate that the tenant code is unique.
        """
        value = value.strip().lower()
        if Tenant.objects.filter(code=value).exists():
            raise serializers.ValidationError(
                "A tenant with this code already exists."
            )

        return value

    def validate_email(self, value: str) -> str:
        """
        Validate that the tenant email is unique.
        """
        value = value.strip().lower()
        if Tenant.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A tenant with this email already exists."
            )

        return value

    def validate_name(self, value: str) -> str:
        """
        Validate that the tenant name is unique.
        """
        value = value.strip().lower()
        if Tenant.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                "A tenant with this name already exists."
            )

        return value
class TenantUpdateSerializer(BaseTenantSerializer):
    """
    Serializer for updating tenant information.

    This serializer validates incoming update data before
    delegating the update operation to the service layer.
    """

    class Meta(BaseTenantSerializer.Meta):
        read_only_fields = (
            "id",
            "code",
            "status",
            "created_at",
            "updated_at",
        )
class TenantSerializer(BaseTenantSerializer):
    """
    Serializer for retrieving tenant details.

    This serializer provides a read-only representation
    of tenant information for list and retrieve APIs.
    """

    class Meta(BaseTenantSerializer.Meta):
        pass
    
class TenantStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for updating tenant status.

    This serializer validates only the tenant status field
    before delegating the status update operation to the
    service layer.
    """

    class Meta:
        model = Tenant
        fields = (
            "status",
        )