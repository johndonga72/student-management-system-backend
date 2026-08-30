
"""
Student serializers.
"""

from rest_framework import serializers

from apps.students.models import Student

from .base import BaseStudentSerializer


class StudentCreateSerializer(BaseStudentSerializer):
    """
    Serializer for student profile creation.
    """

    class Meta(BaseStudentSerializer.Meta):
        model = Student

        fields = (
            "date_of_birth",
            "gender",
            "phone",
            "address",
            "guardian_name",
            "guardian_phone",
        )


class StudentUpdateSerializer(BaseStudentSerializer):
    """
    Serializer for updating student profile.
    """

    class Meta(BaseStudentSerializer.Meta):
        model = Student

        fields = (
            "date_of_birth",
            "gender",
            "phone",
            "address",
            "guardian_name",
            "guardian_phone",
        )


class StudentApprovalSerializer(serializers.ModelSerializer):
    """
    Serializer for approving a student.
    """

    class Meta:
        model = Student

        fields = (
            "department",
            "course",
            "semester",
            "section",
            "admission_date",
            "status",
        )

        read_only_fields = (
            "status",
        )

    def validate(self, attrs):
        """
        Validate tenant ownership and
        department-course relationship.
        """
        print(
                "GET_TENANT CALLED:",
                self.__class__.__name__,
                self.context,
            )
        tenant = self.context.get("tenant")

        if tenant is None:
            raise serializers.ValidationError(
                "Tenant context is required."
            )

        department = attrs.get("department")
        course = attrs.get("course")

        # -----------------------------------------------
        # Validate department tenant
        # -----------------------------------------------

        if department:
            if department.tenant_id != tenant.id:
                raise serializers.ValidationError(
                    {
                        "department": (
                            "Selected department does not "
                            "belong to this tenant."
                        )
                    }
                )

            if department.is_deleted:
                raise serializers.ValidationError(
                    {
                        "department": (
                            "Selected department has "
                            "been deleted."
                        )
                    }
                )

            if not department.is_active:
                raise serializers.ValidationError(
                    {
                        "department": (
                            "Selected department is inactive."
                        )
                    }
                )

        # -----------------------------------------------
        # Validate course tenant
        # -----------------------------------------------

        if course:
            if course.tenant_id != tenant.id:
                raise serializers.ValidationError(
                    {
                        "course": (
                            "Selected course does not "
                            "belong to this tenant."
                        )
                    }
                )

            if course.is_deleted:
                raise serializers.ValidationError(
                    {
                        "course": (
                            "Selected course has "
                            "been deleted."
                        )
                    }
                )

            if not course.is_active:
                raise serializers.ValidationError(
                    {
                        "course": (
                            "Selected course is inactive."
                        )
                    }
                )

        # -----------------------------------------------
        # Validate course -> department relationship
        # -----------------------------------------------

        if (
            department
            and course
            and course.department_id != department.id
        ):
            raise serializers.ValidationError(
                {
                    "course": (
                        "Selected course does not belong "
                        "to the selected department."
                    )
                }
            )

        return attrs


class StudentStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for updating student status.
    """

    class Meta:
        model = Student

        fields = (
            "status",
        )


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for student details.
    """

    user = serializers.StringRelatedField()
    department = serializers.StringRelatedField()
    course = serializers.StringRelatedField()

    class Meta:
        model = Student

        fields = (
            "id",
            "student_number",
            "user",
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
            "created_at",
            "updated_at",
        )

        read_only_fields = fields