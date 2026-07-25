"""
Base serializer for the Teacher module.

This module contains the reusable serializer used
for representing teacher information.
"""
from rest_framework import serializers
from apps.teachers.models import Teacher
class BaseTeacherSerializer(serializers.ModelSerializer):
    """
    Base serializer for representing teacher information.
    """
    teacher_name = serializers.CharField(
        source="user.get_full_name",
        read_only=True,
    )
    email = serializers.EmailField(
        source="user.email",
        read_only=True,
    )
    phone_number = serializers.CharField(
        source="user.phone_number",
        read_only=True,
    )
    department = serializers.StringRelatedField()
    subjects = serializers.StringRelatedField(
        many=True,
    )
    class Meta:
        model = Teacher
        fields = (
            "id",
            "teacher_name",
            "email",
            "phone_number",
            "employee_id",
            "department",
            "designation",
            "qualification",
            "specialization",
            "experience_years",
            "joining_date",
            "subjects",
            "is_active",
        )
        read_only_fields = fields