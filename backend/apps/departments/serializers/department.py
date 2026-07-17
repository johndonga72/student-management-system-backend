"""
Serializers for department-related operations.
"""
from rest_framework import serializers
from apps.departments.models import Department
class DepartmentCreateSerializer(serializers.ModelSerializer):
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
        Validate that the department name is unique.
        """
        if Department.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError(
                "A department with this name already exists."
            )
        return value.strip()
    def validate_code(self, value: str) -> str:
        """
        Validate that the department code is unique.
        """
        code = value.strip().upper()
        if Department.objects.filter(code__iexact=code).exists():
            raise serializers.ValidationError(
                "A department with this code already exists."
            )
        return code
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
    
class DepartmentUpdateSerializer(serializers.ModelSerializer):
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
        Validate that the department name remains unique.
        """
        value = value.strip()
        queryset = Department.objects.filter(name__iexact=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError(
                "A department with this name already exists."
            )
        return value
    def validate_code(self, value: str) -> str:
        """
        Validate that the department code remains unique.
        """
        value = value.strip().upper()
        queryset = Department.objects.filter(code__iexact=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError(
                "A department with this code already exists."
            )
        return value