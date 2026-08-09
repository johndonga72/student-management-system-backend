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
    """
    Service class containing student-related business logic.
    """

    # ======================================================
    # Private Helper Methods
    # ======================================================

    @staticmethod
    def _get_student_object(
        tenant,
        student_id: int,
    ) -> Student:
        """
        Retrieve a student belonging to the current tenant.

        Args:
            tenant:
                Current tenant.

            student_id:
                Student primary key.

        Returns:
            Student:
                Tenant-scoped student instance.

        Raises:
            ValidationError:
                If the student does not exist in the tenant.
        """

        try:
            return (
                Student.objects
                .for_tenant(tenant)
                .select_related(
                    "user",
                    "department",
                    "course",
                )
                .get(
                    pk=student_id,
                    is_deleted=False,
                )
            )

        except Student.DoesNotExist as exc:
            raise ValidationError(
                "Student does not exist."
            ) from exc

    @staticmethod
    def _student_profile_exists(
        tenant,
        user: CustomUser,
    ) -> bool:
        """
        Check whether a student profile already exists
        for the user within the current tenant.

        Args:
            tenant:
                Current tenant.

            user:
                Authenticated user.

        Returns:
            bool:
                True if a profile exists; otherwise False.
        """

        return (
            Student.objects
            .for_tenant(tenant)
            .filter(
                user=user,
                is_deleted=False,
            )
            .exists()
        )

    @staticmethod
    def _generate_student_number() -> str:
        """
        Generate the next globally unique student number.

        Student numbers are intentionally NOT tenant-scoped.

        Returns:
            str:
                Generated student number.
        """

        latest_student = (
            Student.objects
            .exclude(
                student_number="",
            )
            .order_by("-id")
            .first()
        )

        if latest_student is None:
            return "ST20260001"

        latest_number = int(
            latest_student.student_number[-4:]
        )

        return f"ST2026{latest_number + 1:04d}"

    @staticmethod
    def _validate_department_course(
        tenant,
        student: Student,
    ) -> None:
        """
        Validate department and course tenant ownership
        and their relationship.

        Args:
            tenant:
                Current tenant.

            student:
                Student instance containing the selected
                department and course.

        Raises:
            ValidationError:
                If department/course belong to another
                tenant or the course does not belong to
                the selected department.
        """

        department = student.department
        course = student.course

        # --------------------------------------------------
        # Department tenant validation
        # --------------------------------------------------

        if department:
            if department.tenant_id != tenant.id:
                raise ValidationError(
                    "The selected department does not "
                    "belong to the current tenant."
                )

            if department.is_deleted:
                raise ValidationError(
                    "The selected department has been deleted."
                )

            if not department.is_active:
                raise ValidationError(
                    "The selected department is inactive."
                )

        # --------------------------------------------------
        # Course tenant validation
        # --------------------------------------------------

        if course:
            if course.tenant_id != tenant.id:
                raise ValidationError(
                    "The selected course does not "
                    "belong to the current tenant."
                )

            if course.is_deleted:
                raise ValidationError(
                    "The selected course has been deleted."
                )

            if not course.is_active:
                raise ValidationError(
                    "The selected course is inactive."
                )

        # --------------------------------------------------
        # Course -> Department relationship
        # --------------------------------------------------

        if (
            department
            and course
            and course.department_id != department.id
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
        tenant,
        user: CustomUser,
        validated_data: dict,
    ) -> Student:
        """
        Create a student profile for the authenticated user
        within the current tenant.

        Args:
            tenant:
                Current tenant.

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

        if StudentService._student_profile_exists(
            tenant=tenant,
            user=user,
        ):
            raise ValidationError(
                "Student profile already exists."
            )

        return Student.objects.create(
            tenant=tenant,
            user=user,
            **validated_data,
        )
    @staticmethod
    def update_student_profile(
        tenant,
        student_id: int,
        validated_data: dict,
    ) -> Student:
        """
        Update the student's editable profile fields.

        Args:
            tenant:
                Current tenant.

            student_id:
                Student primary key.

            validated_data:
                Validated serializer data.

        Returns:
            Student:
                Updated student profile.
        """

        student = StudentService._get_student_object(
            tenant=tenant,
            student_id=student_id,
        )

        editable_fields = (
            "date_of_birth",
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
        tenant,
        student_id: int,
    ) -> Student:
        """
        Retrieve a student by ID within the current tenant.

        Args:
            tenant:
                Current tenant.

            student_id:
                Student primary key.

        Returns:
            Student:
                Requested student.
        """

        return StudentService._get_student_object(
            tenant=tenant,
            student_id=student_id,
        )
    @staticmethod
    def get_my_profile(
        tenant,
        user: CustomUser,
    ) -> Student:
        """
        Retrieve the authenticated user's student profile
        within the current tenant.

        Args:
            tenant:
                Current tenant.

            user:
                Authenticated user.

        Returns:
            Student:
                Student profile.
        """

        try:
            return (
                Student.objects
                .for_tenant(tenant)
                .select_related(
                    "user",
                    "department",
                    "course",
                )
                .get(
                    user=user,
                    is_deleted=False,
                )
            )

        except Student.DoesNotExist as exc:
            raise ValidationError(
                "Student profile not found."
            ) from exc
    @staticmethod
    def list_students(
        tenant,
    ):
        """
        Retrieve all active student profiles
        belonging to the current tenant.

        Args:
            tenant:
                Current tenant.

        Returns:
            QuerySet[Student]:
                Tenant-scoped student queryset.
        """

        return (
            Student.objects
            .for_tenant(tenant)
            .select_related(
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
    def list_pending_students(
        tenant,
    ):
        """
        Retrieve all pending student profiles
        belonging to the current tenant.

        Args:
            tenant:
                Current tenant.

        Returns:
            QuerySet[Student]:
                Tenant-scoped pending students.
        """

        return (
            Student.objects
            .for_tenant(tenant)
            .select_related(
                "user",
                "department",
                "course",
            )
            .filter(
                status=StudentStatus.PENDING,
                is_deleted=False,
            )
            .order_by(
                "student_number",
            )
        )


    @staticmethod
    def approve_student(
        tenant,
        student_id: int,
        validated_data: dict,
    ) -> Student:
        """
        Approve a pending student profile.

        Args:
            tenant:
                Current tenant.

            student_id:
                Student primary key.

            validated_data:
                Academic information assigned by
                the administrator.

        Returns:
            Student:
                Approved student profile.
        """

        # --------------------------------------------------
        # Retrieve tenant-scoped student
        # --------------------------------------------------

        student = StudentService._get_student_object(
            tenant=tenant,
            student_id=student_id,
        )

        # --------------------------------------------------
        # Ensure only pending students are approved
        # --------------------------------------------------

        if student.status != StudentStatus.PENDING:
            raise ValidationError(
                "Only pending students can be approved."
            )

        # --------------------------------------------------
        # Extract academic information
        # --------------------------------------------------

        department = validated_data["department"]
        course = validated_data["course"]
        semester = validated_data["semester"]

        # --------------------------------------------------
        # Validate department and course
        # --------------------------------------------------

        if department.tenant_id != tenant.id:
            raise ValidationError(
                "The selected department does not "
                "belong to the current tenant."
            )

        if course.tenant_id != tenant.id:
            raise ValidationError(
                "The selected course does not "
                "belong to the current tenant."
            )

        if department.is_deleted:
            raise ValidationError(
                "The selected department has been deleted."
            )

        if not department.is_active:
            raise ValidationError(
                "The selected department is inactive."
            )

        if course.is_deleted:
            raise ValidationError(
                "The selected course has been deleted."
            )

        if not course.is_active:
            raise ValidationError(
                "The selected course is inactive."
            )

        # --------------------------------------------------
        # Validate course -> department relationship
        # --------------------------------------------------

        if course.department_id != department.id:
            raise ValidationError(
                "The selected course does not belong "
                "to the selected department."
            )

        # --------------------------------------------------
        # Validate semester
        # --------------------------------------------------

        StudentService._validate_semester(
            semester,
        )

        # --------------------------------------------------
        # Assign academic information
        # --------------------------------------------------

        student.department = department
        student.course = course
        student.semester = semester
        student.section = validated_data.get(
            "section",
        )
        student.admission_date = validated_data[
            "admission_date"
        ]

        # --------------------------------------------------
        # Generate globally unique student number
        # --------------------------------------------------

        student.student_number = (
            StudentService._generate_student_number()
        )

        student.status = StudentStatus.APPROVED

        student.save()

        return student


    @staticmethod
    def change_student_status(
        tenant,
        student_id: int,
        status: StudentStatus,
    ) -> Student:
        """
        Update a student's status.

        Args:
            tenant:
                Current tenant.

            student_id:
                Student primary key.

            status:
                New student status.

        Returns:
            Student:
                Updated student profile.
        """

        student = StudentService._get_student_object(
            tenant=tenant,
            student_id=student_id,
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
        tenant,
        student_id: int,
    ) -> None:
        """
        Soft delete a student profile.

        Args:
            tenant:
                Current tenant.

            student_id:
                Student primary key.
        """

        student = StudentService._get_student_object(
            tenant=tenant,
            student_id=student_id,
        )

        student.is_deleted = True

        student.save(
            update_fields=[
                "is_deleted",
                "updated_at",
            ]
        )
