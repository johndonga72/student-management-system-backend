
"""
Base serializer for student validations.
"""

from django.utils import timezone

from rest_framework import serializers

from apps.students.models import Student


class BaseStudentSerializer(serializers.ModelSerializer):
    """
    Base serializer containing reusable validation logic.
    """

    class Meta:
        model = Student

        fields = (
            "id",
            "user",
            "student_number",
            "department",
            "course",
            "semester",
            "section",
            "date_of_birth",
            "gender",
            "phone",
            "address",
            "guardian_name",
            "guardian_phone",
            "admission_date",
            "status",
            "is_deleted",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "student_number",
            "status",
            "is_deleted",
            "created_at",
            "updated_at",
        )

    def validate_department(self, department):
        """
        Validate that the department belongs
        to the current tenant.
        """

        tenant = self.context.get("tenant")

        if tenant is None:
            raise serializers.ValidationError(
                "Tenant context is required."
            )

        if department.tenant_id != tenant.id:
            raise serializers.ValidationError(
                "Selected department does not belong to this tenant."
            )

        if not department.is_active:
            raise serializers.ValidationError(
                "Selected department is inactive."
            )

        if department.is_deleted:
            raise serializers.ValidationError(
                "Selected department has been deleted."
            )

        return department

    def validate_course(self, course):
        """
        Validate that the course belongs
        to the current tenant.
        """

        tenant = self.context.get("tenant")

        if tenant is None:
            raise serializers.ValidationError(
                "Tenant context is required."
            )

        if course.tenant_id != tenant.id:
            raise serializers.ValidationError(
                "Selected course does not belong to this tenant."
            )

        if not course.is_active:
            raise serializers.ValidationError(
                "Selected course is inactive."
            )

        if course.is_deleted:
            raise serializers.ValidationError(
                "Selected course has been deleted."
            )

        return course

    def validate_date_of_birth(self, value):
        """
        Validate date of birth.
        """

        if value >= timezone.now().date():
            raise serializers.ValidationError(
                "Date of birth must be in the past."
            )

        return value

    def validate_phone(self, value: str) -> str:
        """
        Validate student phone number.
        """

        if len(value) != 10 or not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain exactly 10 digits."
            )

        return value

    def validate_guardian_phone(self, value: str) -> str:
        """
        Validate guardian phone number.
        """

        if len(value) != 10 or not value.isdigit():
            raise serializers.ValidationError(
                "Guardian phone number must contain exactly 10 digits."
            )

        return value