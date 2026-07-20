"""
Serializers for course-related operations.
"""
from __future__ import annotations
from rest_framework import serializers
from apps.courses.models import Course
class BaseCourseSerializer(serializers.ModelSerializer):
    """
    Base serializer containing shared validation
    for course create and update operations.
    """
    class Meta:
        model = Course
        fields = (
            "department",
            "name",
            "code",
            "description",
            "credits",
        )
        extra_kwargs = {
            "name": {
                "error_messages": {
                    "required": "Course name is required.",
                    "blank": "Course name cannot be empty.",
                }
            },
            "code": {
                "error_messages": {
                    "required": "Course code is required.",
                    "blank": "Course code cannot be empty.",
                }
            },
            "credits": {
                "error_messages": {
                    "required": "Course credits are required.",
                }
            },
        }
    def validate_department(self, department):
        """
        Validate the selected department.
        """
        if department.is_deleted:
            raise serializers.ValidationError(
                "Selected department has been deleted."
            )
        if not department.is_active:
            raise serializers.ValidationError(
                "Selected department is inactive."
            )
        return department
    def validate_name(self, value):
        """
        Validate course name.
        """
        value = value.strip()
        if not value:
            raise serializers.ValidationError(
                "Course name cannot be empty."
            )
        return value
    def validate_code(self, value):
        """
        Validate course code.
        """
        value = value.strip().upper()
        if not value:
            raise serializers.ValidationError(
                "Course code cannot be empty."
            )
        return value

    def validate_credits(self, value):
        """
        Validate course credits.
        """
        if value <= 0:
            raise serializers.ValidationError(
                "Credits must be greater than zero."
            )
        return value
class CourseCreateSerializer(BaseCourseSerializer):
    """
    Serializer for creating a course.
    """
    pass
class CourseUpdateSerializer(BaseCourseSerializer):
    """
    Serializer for updating a course.
    """
    pass
class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for course details.
    """
    department = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = (
            "id",
            "department",
            "name",
            "code",
            "description",
            "credits",
            "is_active",
            "created_at",
            "updated_at",
        )
    def get_department(self, obj):
        """
        Return department details.
        """
        return {
            "id": obj.department.id,
            "name": obj.department.name,
        }
class CourseStatusSerializer(serializers.Serializer):
    """
    Serializer for updating course status.
    """
    is_active = serializers.BooleanField()
