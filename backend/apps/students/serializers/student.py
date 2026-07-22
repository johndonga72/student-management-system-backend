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
    def validate(self, attrs):
        """
        Validate department and course relationship.
        """
        department = attrs.get("department")
        course = attrs.get("course")
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
