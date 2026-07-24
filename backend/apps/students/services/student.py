"""
Service layer for student-related business operations.

This module contains business logic for creating, updating,
approving, retrieving, and managing student profiles.
"""
from __future__ import annotations
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError
from apps.accounts.models import CustomUser
from apps.students.models import (
    Student,
    StudentStatus,
)
class StudentService:
    # ======================================================
    # Private Helper Methods
    # ======================================================
    @staticmethod
    def _get_student_object(
        student_id: int,
    ) -> Student:
        """
        Retrieve a student by its primary key.

        Args:
            student_id:
                Student primary key.

        Returns:
            Student:
                Student instance.

        Raises:
            ValidationError:
                If the student does not exist.
        """

        try:
            return Student.objects.select_related(
                "user",
                "department",
                "course",
            ).get(
                pk=student_id,
                is_deleted=False,
            )

        except Student.DoesNotExist as exc:
            raise ValidationError(
                "Student does not exist."
            ) from exc
    @staticmethod
    def _student_profile_exists(
        user: CustomUser,
    ) -> bool:
        """
        Check whether a student profile already exists.

        Args:
            user:
                Authenticated user.

        Returns:
            bool:
                True if a profile exists; otherwise False.
        """

        return Student.objects.filter(
            user=user,
            is_deleted=False,
        ).exists()
        
    @staticmethod
    def _generate_student_number() -> str:
        """
        Generate the next unique student number.

        Returns:
            str:
                Generated student number.
        """

        latest_student = (
        Student.objects.exclude(
        student_number=""
        ).order_by("-id").first()
        )

        if latest_student is None:
            return "ST20260001"

        latest_number = int(
            latest_student.student_number[-4:]
        )

        return f"ST2026{latest_number + 1:04d}"
    @staticmethod
    def _validate_department_course(
        student: Student,
    ) -> None:
        """
        Validate that the selected course belongs to
        the selected department.

        Args:
            student:
                Student instance.

        Raises:
            ValidationError:
                If the course does not belong to the department.
        """
        if (
            student.department
            and student.course
            and student.course.department_id
            != student.department.id
        ):
            raise ValidationError(
                "The selected course does not belong "
                "to the selected department."
            )
    @staticmethod
    def _validate_semester(
        semester: int,
    ) -> None:
        """
        Validate semester value.
        Args:
            semester:
                Semester number.

        Raises:
            ValidationError:
                If semester is invalid.
        """
        if semester < 1 or semester > 8:
            raise ValidationError(
                "Semester must be between 1 and 8."
            )
# ======================================================
# Public Business Methods
# ======================================================
    @staticmethod
    def create_student_profile(
        user: CustomUser,
        validated_data: dict,
    ) -> Student:
        """
        Create a student profile for the authenticated user.

        Args:
            user:
                Authenticated user.

            validated_data:
                Validated serializer data.

        Returns:
            Student:
                Newly created student profile.

        Raises:
            ValidationError:
                If the student profile already exists.
        """

        if StudentService._student_profile_exists(user):
            raise ValidationError(
                "Student profile already exists."
            )

        return Student.objects.create(
            user=user,
            **validated_data,
        )
    @staticmethod
    def update_student_profile(
        student: Student,
        validated_data: dict,
    ) -> Student:
        """
        Update the student's editable profile fields.
        """
        editable_fields = (
                   "date_of_birth"
                    "gender",
                    "phone",
                    "address",
                    "guardian_name",
                    "guardian_phone",
        )
        for field in editable_fields:
            if field in validated_data:
                setattr(
                    student,
                    field,
                    validated_data[field],
                )
        student.save()
        return student
    @staticmethod
    def get_student_by_id(
        student_id: int,
    ) -> Student:
        """
        Retrieve a student by ID.

        Args:
            student_id:
                Student primary key.

        Returns:
            Student:
                Requested student.
        """

        return StudentService._get_student_object(
            student_id,
        )
    @staticmethod
    def get_my_profile(
        user: CustomUser,
    ) -> Student:
        """
        Retrieve the authenticated user's student profile.

        Args:
            user:
                Authenticated user.

        Returns:
            Student:
                Student profile.
        """

        try:
            return Student.objects.select_related(
                "department",
                "course",
            ).get(
                user=user,
                is_deleted=False,
            )

        except Student.DoesNotExist as exc:
            raise ValidationError(
                "Student profile not found."
            ) from exc
    @staticmethod
    def list_students():
        """
        Retrieve all active student profiles.

        Returns:
            QuerySet[Student]:
                Student queryset.
        """

        return (
            Student.objects.select_related(
                "user",
                "department",
                "course",
            )
            .filter(
                is_deleted=False,
            )
            .order_by(
                "student_number",
            )
        )
    @staticmethod
    def list_pending_students():
        """
        Retrieve all pending student profiles.

        Returns:
            QuerySet[Student]:
                Pending students.
        """

        return (
            Student.objects.select_related(
                "user",
                "department",
                "course",
            )
            .filter(
                status=StudentStatus.PENDING,
                is_deleted=False,
            )
        )
    @staticmethod
    def approve_student(
        student_id: int,
        validated_data: dict,
    ) -> Student:
        """
        Approve a pending student profile.

        Args:
            student_id:
                Student primary key.

            validated_data:
                Academic information assigned by the administrator.

        Returns:
            Student:
                Approved student profile.
        """

        student = StudentService._get_student_object(
            student_id,
        )

        department = validated_data["department"]
        course = validated_data["course"]
        semester = validated_data["semester"]

        StudentService._validate_department_course(
         student
        )

        StudentService._validate_semester(
            semester,
        )

        student.department = department
        student.course = course
        student.semester = semester
        student.section = validated_data.get(
            "section",
        )
        student.admission_date = validated_data[
            "admission_date"
        ]
        student.status = StudentStatus.APPROVED
        student.student_number = (
            StudentService._generate_student_number()
        )
        student.save()
        return student
    @staticmethod
    def change_student_status(
        student_id: int,
        status: StudentStatus,
    ) -> Student:
        """
        Update a student's status.

        Args:
            student_id:
                Student primary key.

            status:
                New student status.

        Returns:
            Student:
                Updated student profile.
        """

        student = StudentService._get_student_object(
            student_id,
        )

        student.status = status

        student.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return student
    @staticmethod
    def delete_student(
        student_id: int,
    ) -> None:
        """
        Soft delete a student profile.

        Args:
            student_id:
                Student primary key.
        """

        student = StudentService._get_student_object(
            student_id,
        )
        student.is_deleted = True
        student.save(
            update_fields=[
                "is_deleted",
                "updated_at",
            ]
        )