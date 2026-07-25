"""
Teacher serializers.
This module contains serializers for creating,
updating, and managing teacher information.
"""
from rest_framework import serializers
from apps.departments.models import Department
from apps.subjects.models import Subject
from apps.teachers.models import Teacher
from .base import BaseTeacherSerializer
class TeacherSerializer(BaseTeacherSerializer):
    """
    Serializer for representing teacher information.
    """
    class Meta(BaseTeacherSerializer.Meta):
        pass
class TeacherCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a teacher profile.
    """
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.filter(
            is_active=True,
            is_deleted=False,
        ),
    )
    subjects = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.filter(
            is_active=True,
            is_deleted=False,
        ),
        many=True,
        required=False,
    )

    class Meta:
        model = Teacher

        fields = (
            "user",
            "department",
            "designation",
            "qualification",
            "specialization",
            "experience_years",
            "joining_date",
            "subjects",
        )

class TeacherUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a teacher profile.
    """
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.filter(
            is_active=True,
            is_deleted=False,
        ),
        required=False,
    )
    subjects = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.filter(
            is_active=True,
            is_deleted=False,
        ),
        many=True,
        required=False,
    )
    class Meta:
        model = Teacher

        fields = (
            "department",
            "designation",
            "qualification",
            "specialization",
            "experience_years",
            "joining_date",
            "subjects",
        )
class TeacherStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for changing teacher status.
    """
    class Meta:
        model = Teacher
        fields = (
            "is_active",
        )