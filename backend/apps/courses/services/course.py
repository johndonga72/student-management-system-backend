"""
Business services for course-related operations.
"""
from __future__ import annotations
from django.core.exceptions import ValidationError
from apps.courses.models import Course
class CourseService:
    @staticmethod
    def _validate_unique_course_code(
        department,
        code: str,
        exclude_course_id: int | None = None,
    ) -> None:
        """
        Validate that the course code is unique within
        the selected department.
        Raises:
            ValidationError:
                If the course code already exists.
        """
        queryset = Course.objects.filter(
            department=department,
            code=code,
            is_deleted=False,
        )
        if exclude_course_id is not None:
            queryset = queryset.exclude(
                id=exclude_course_id
            )
        if queryset.exists():
            raise ValidationError(
                "A course with this code already exists in the selected department."
            )
    @staticmethod
    def _get_course(
        course_id: int,
    ) -> Course:
        """
        Retrieve a course by its ID.

        Raises:
            ValidationError:
                If the course does not exist.
        """

        try:
            return Course.objects.select_related(
                "department",
            ).get(
                pk=course_id,
                is_deleted=False,
            )

        except Course.DoesNotExist:
            raise ValidationError(
                "Course does not exist."
            )
    @staticmethod
    def create_course(
        validated_data: dict,
    ) -> Course:
        """
        Create a new course.
        """
        CourseService._validate_unique_course_code(
            department=validated_data["department"],
            code=validated_data["code"],
        )
        return Course.objects.create(
            **validated_data
        )
    @staticmethod
    def update_course(
        course_id: int,
        validated_data: dict,
    ) -> Course:
        """
        Update an existing course.
        """
        course = CourseService.get_course_by_id(
            course_id
        )
        department = validated_data.get(
            "department",
            course.department,
        )
        code = validated_data.get(
            "code",
            course.code,
        )
        CourseService._validate_unique_course_code(
            department=department,
            code=code,
            exclude_course_id=course.id,
        )
        for field, value in validated_data.items():
            setattr(course, field, value)
        course.save()
        return course
    @staticmethod
    def list_courses():
        """
        Return all non-deleted courses.
        """
        return Course.objects.filter(
            is_deleted=False,
        ).select_related(
            "department",
        ).order_by(
            "name",
        )
    @staticmethod
    def get_course_by_id(
        course_id: int,
    ) -> Course:
        """
        Retrieve a course by its ID.
        """

        return CourseService._get_course(course_id)
    @staticmethod
    def change_course_status(
        course_id: int,
        is_active: bool,
    ) -> Course:
        """
        Activate or deactivate a course.
        Args:
            course_id: Course primary key.
            is_active: Course status.
        Returns:
            Course: Updated course instance.
        """
        course = CourseService._get_course(course_id)
        course.is_active = is_active
        course.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )
        return course 
    @staticmethod
    def delete_course(
        course_id: int,
    ) -> None:
        """
        Soft delete a course.
        """
        course = CourseService._get_course(course_id)
        course.is_deleted = True
        course.save(
            update_fields=[
                "is_deleted",
                "updated_at",
            ]
        )
