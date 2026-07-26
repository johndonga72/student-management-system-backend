"""
Teacher service.

This module contains the business logic for
managing teacher operations.
"""

from __future__ import annotations

from typing import Iterable

from django.db import transaction
from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from apps.accounts.models import CustomUser
from apps.accounts.models import UserRole
from apps.departments.models import Department
from apps.subjects.models import Subject
from apps.teachers.models import Teacher


class TeacherService:
    """
    Service class responsible for teacher-related
    business operations.
    """

    # ==========================================================
    # Private Helper Methods
    # ==========================================================

    @classmethod
    def _get_teacher(
        cls,
        teacher_id: int,
    ) -> Teacher:
        """
        Retrieve an active teacher by identifier.

        Args:
            teacher_id: Unique identifier of the teacher.

        Returns:
            Teacher: The matching teacher instance.

        Raises:
            ValidationError: If the teacher does not exist or
                has been deleted.
        """
        try:
            return (
                Teacher.objects.select_related(
                    "user",
                    "department",
                )
                .prefetch_related(
                    "subjects",
                )
                .get(
                    id=teacher_id,
                    is_deleted=False,
                )
            )

        except Teacher.DoesNotExist as exc:
            raise ValidationError(
                {
                    "teacher": (
                        "Teacher does not exist."
                    ),
                }
            ) from exc

    @classmethod
    def _validate_teacher_user(
        cls,
        user: CustomUser,
    ) -> CustomUser:
        """
        Validate whether the given user is eligible
        to become a teacher.

        Args:
            user: User instance to validate.

        Returns:
            CustomUser: The validated user instance.

        Raises:
            ValidationError: If the user is not eligible
                to become a teacher.
        """
        if not user:
            raise ValidationError(
                {
                    "user": (
                        "User does not exist."
                    ),
                }
            )

        if getattr(user, "is_deleted", False):
            raise ValidationError(
                {
                    "user": (
                        "Deleted users cannot be assigned as teachers."
                    ),
                }
            )

        if Teacher.objects.filter(
            user=user,
            is_deleted=False,
        ).exists():
            raise ValidationError(
                {
                    "user": (
                        "A teacher profile already exists for this user."
                    ),
                }
            )

        return user

    @classmethod
    def _validate_department(
        cls,
        department: Department,
    ) -> Department:
        """
        Validate the assigned department.

        Args:
            department: Department assigned to the teacher.

        Returns:
            Department: The validated department.

        Raises:
            ValidationError: If the department is inactive
                or has been deleted.
        """
        if department.is_deleted:
            raise ValidationError(
                {
                    "department": (
                        "The selected department has been deleted."
                    ),
                }
            )

        if not department.is_active:
            raise ValidationError(
                {
                    "department": (
                        "The selected department is inactive."
                    ),
                }
            )
        return department

    @classmethod
    def _validate_subjects(
        cls,
        department: Department,
        subjects: Iterable[Subject],
    ) -> list[Subject]:
        """
        Validate the subjects assigned to the teacher.

        Args:
            department: Department assigned to the teacher.
            subjects: Subjects selected for the teacher.

        Returns:
            list[Subject]: Validated subject instances.

        Raises:
            ValidationError: If any subject is inactive,
                deleted, or does not belong to the
                specified department.
        """
        validated_subjects = []

        for subject in subjects:

            if subject.is_deleted:
                raise ValidationError(
                    {
                        "subjects": (
                            f"Subject '{subject.subject_name}' "
                            "has been deleted."
                        ),
                    }
                )

            if not subject.is_active:
                raise ValidationError(
                    {
                        "subjects": (
                            f"Subject '{subject.subject_name}' "
                            "is inactive."
                        ),
                    }
                )

            if subject.course.department_id != department.id:
                raise ValidationError(
                    {
                        "subjects": (
                            f"Subject '{subject.subject_name}' "
                            "does not belong to the selected department."
                        ),
                    }
                )

            validated_subjects.append(subject)

        return validated_subjects

    @classmethod
    def _generate_employee_id(cls) -> str:
        """
        Generate the next unique employee identifier.

        Returns:
            str: Newly generated employee identifier.
        """
        last_teacher = (
            Teacher.objects.order_by("-id")
            .only("employee_id")
            .first()
        )
        if last_teacher is None:
            return "EMP0001"
        last_number = int(
            last_teacher.employee_id.replace(
                "EMP",
                "",
            )
        )
        return f"EMP{last_number + 1:04d}"

    @classmethod
    def _promote_user_to_teacher(
        cls,
        user: CustomUser,
    ) -> None:
        """
        Promote a user from STUDENT to TEACHER.

        Args:
            user: User to promote.
        """
        if user.role == UserRole.TEACHER:
            return

        user.role = UserRole.TEACHER
        user.save(update_fields=["role"])

    # ==========================================================
    # Public Business Methods
    # ==========================================================
    @classmethod
    @transaction.atomic
    def create_teacher(
        cls,
        validated_data: dict,
    ) -> Teacher:
        """
        Create a teacher profile.

        Args:
            validated_data: Validated serializer data.

        Returns:
            Teacher: Newly created teacher profile.
        """
        subjects = validated_data.pop("subjects", [])

        user = cls._validate_teacher_user(validated_data["user"])
        department = cls._validate_department(validated_data["department"])

        validated_subjects = cls._validate_subjects(
            department,
            subjects,
        )

        validated_data["user"] = user
        validated_data["department"] = department
        validated_data["employee_id"] = cls._generate_employee_id()

        teacher = Teacher.objects.create(
            **validated_data,
        )

        teacher.subjects.set(validated_subjects)

        cls._promote_user_to_teacher(user)

        return teacher
    @classmethod
    def get_teacher_by_id(
        cls,
        teacher_id: int,
    ) -> Teacher:
        """
        Retrieve a teacher by identifier.

        Args:
            teacher_id: Unique teacher identifier.

        Returns:
            Teacher: Matching teacher instance.
        """
        return cls._get_teacher(teacher_id)

    @classmethod
    def list_teachers(cls) -> QuerySet[Teacher]:
        """
        Retrieve all active teacher profiles.

        Returns:
            QuerySet[Teacher]: Teacher queryset.
        """
        return (
            Teacher.objects.select_related(
                "user",
                "department",
            )
            .prefetch_related(
                "subjects",
            )
            .filter(
                is_deleted=False,
            )
            .order_by("employee_id")
        )
    @classmethod
    @transaction.atomic
    def update_teacher(
        cls,
        teacher_id: int,
        validated_data: dict,
    ) -> Teacher:
        """
        Update an existing teacher profile.
        """
        teacher = cls._get_teacher(teacher_id)

        subjects = validated_data.pop(
            "subjects",
            None,
        )

        if "department" in validated_data:
            validated_data["department"] = (
                cls._validate_department(
                    validated_data["department"]
                )
            )

        if subjects is not None:
            department = validated_data.get(
                "department",
                teacher.department,
            )

            validated_subjects = cls._validate_subjects(
                department,
                subjects,
            )

            teacher.subjects.set(
                validated_subjects,
            )
        EDITABLE_FIELDS = {
        "department",
        "designation",
        "qualification",
        "specialization",
        "experience_years",
        "joining_date",
        }
        for field in EDITABLE_FIELDS:
            if field in validated_data:
                setattr(
                    teacher,
                    field,
                    validated_data[field],
                )
        teacher.save()
        return teacher
    @classmethod
    def change_teacher_status(
        cls,
        teacher_id: int,
        is_active: bool,
    ) -> Teacher:
        """
        Activate or deactivate a teacher.
        """
        teacher = cls._get_teacher(
            teacher_id,
        )

        teacher.is_active = is_active

        teacher.save(
            update_fields=[
                "is_active",
            ]
        )

        return teacher
    @classmethod
    def delete_teacher(
        cls,
        teacher_id: int,
    ) -> None:
        """
        Soft delete a teacher profile.
        """
        teacher = cls._get_teacher(
            teacher_id,
        )

        teacher.is_deleted = True

        teacher.save(
            update_fields=[
                "is_deleted",
            ]
        )