"""
Business services for course-related operations.
"""

from __future__ import annotations

from rest_framework.exceptions import ValidationError

from apps.courses.models import Course


class CourseService:
    """
    Service class containing business logic for course operations.
    """

    @staticmethod
    def _validate_unique_course_code(
        tenant,
        department,
        code: str,
        exclude_course_id: int | None = None,
    ) -> None:
        """
        Validate that the course code is unique within
        the selected department and tenant.
        """

        if department.tenant_id != tenant.id:
            raise ValidationError(
                "Selected department does not belong to this tenant."
            )

        queryset = Course.objects.for_tenant(
            tenant
        ).filter(
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
                "A course with this code already exists "
                "in the selected department."
            )

    @staticmethod
    def _get_course(
        tenant,
        course_id: int,
    ) -> Course:
        """
        Retrieve a course within the current tenant.

        Raises:
            ValidationError:
                If the course does not exist.
        """

        try:
            return (
                Course.objects
                .for_tenant(tenant)
                .select_related("department")
                .get(
                    pk=course_id,
                    is_deleted=False,
                )
            )

        except Course.DoesNotExist:
            raise ValidationError(
                "Course does not exist."
            )

    @staticmethod
    def create_course(
        tenant,
        validated_data: dict,
    ) -> Course:
        """
        Create a new course for the current tenant.
        """

        department = validated_data["department"]

        CourseService._validate_unique_course_code(
            tenant=tenant,
            department=department,
            code=validated_data["code"],
        )

        return Course.objects.create(
            tenant=tenant,
            **validated_data,
        )

    @staticmethod
    def update_course(
        tenant,
        course_id: int,
        validated_data: dict,
    ) -> Course:
        """
        Update an existing course within the current tenant.
        """

        course = CourseService.get_course_by_id(
            tenant=tenant,
            course_id=course_id,
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
            tenant=tenant,
            department=department,
            code=code,
            exclude_course_id=course.id,
        )

        for field, value in validated_data.items():
            setattr(course, field, value)

        course.save()

        return course

    @staticmethod
    def list_courses(
        tenant,
    ):
        """
        Return all non-deleted courses
        belonging to the current tenant.
        """

        return (
            Course.objects
            .for_tenant(tenant)
            .filter(
                is_deleted=False,
            )
            .select_related(
                "department",
            )
            .order_by(
                "name",
            )
        )

    @staticmethod
    def get_course_by_id(
        tenant,
        course_id: int,
    ) -> Course:
        """
        Retrieve a course within the current tenant.
        """

        return CourseService._get_course(
            tenant=tenant,
            course_id=course_id,
        )

    @staticmethod
    def change_course_status(
        tenant,
        course_id: int,
        is_active: bool,
    ) -> Course:
        """
        Activate or deactivate a course.
        """

        course = CourseService._get_course(
            tenant=tenant,
            course_id=course_id,
        )

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
        tenant,
        course_id: int,
    ) -> None:
        """
        Soft delete a course within the current tenant.
        """

        course = CourseService._get_course(
            tenant=tenant,
            course_id=course_id,
        )

        course.is_deleted = True

        course.save(
            update_fields=[
                "is_deleted",
                "updated_at",
            ]
        )