"""
Business logic for result management.
"""
from rest_framework.exceptions import ValidationError
from apps.results.models import Result, choices
from apps.students.models import Student
from apps.students.models.choices import StudentStatus
from apps.examinations.models import Examination, ExaminationStatus
from django.db.models import QuerySet
from django.db import transaction
from apps.tenants.models import Tenant
from apps.results.models.choices import (
    ResultStatus,
    ResultRecordStatus,
)
class ResultService:
    """
    Service layer for managing results.
    """

    # ==========================================================
    # Private Helper Methods
    # ==========================================================
    @classmethod
    def _get_result(
        cls,
        tenant: Tenant,
        result_id: int,
    ) -> Result:
        """
        Retrieve a result belonging to the current tenant.

        Args:
            tenant:
                Current tenant.

            result_id:
                Result identifier.

        Returns:
            Result:
                Tenant-scoped result instance.

        Raises:
            ValidationError:
                If the result does not exist
                within the current tenant.
        """

        try:
            return (
                Result.objects
                .for_tenant(tenant)
                .select_related(
                    "student__user",
                    "examination__subject",
                    "examination__teacher__user",
                )
                .get(
                    id=result_id,
                    is_deleted=False,
                )
            )
        except Result.DoesNotExist as exc:
            raise ValidationError(
                {
                    "result": (
                        "Result not found."
                    ),
                }
            ) from exc
    @classmethod
    def _validate_student(
        cls,
        tenant: Tenant,
        student: Student,
    ) -> Student:
        """
        Validate that the student belongs to the
        current tenant and is eligible for a result.

        Args:
            tenant:
                Current tenant.

            student:
                Student instance.

        Returns:
            Student:
                Validated student.

        Raises:
            ValidationError:
                If the student does not belong to
                the tenant, is deleted, or is not approved.
        """

        if student.tenant_id != tenant.id:
            raise ValidationError(
                {
                    "student": (
                        "Student does not belong "
                        "to the current tenant."
                    ),
                }
            )
        if student.is_deleted:
            raise ValidationError(
                {
                    "student": (
                        "Student not found."
                    ),
                }
            )
        if student.status != StudentStatus.APPROVED:
            raise ValidationError(
                {
                    "student": (
                        "Student is not approved."
                    ),
                }
            )
        return student
    @classmethod
    def _validate_examination(
        cls,
        tenant: Tenant,
        examination: Examination,
    ) -> Examination:
        """
        Validate that the examination belongs to the
        current tenant and is active.
        Args:
            tenant:
                Current tenant.
            examination:
                Examination instance.
        Returns:
            Examination:
                Validated examination.
        Raises:
            ValidationError:
                If the examination does not belong
                to the tenant, is deleted, or inactive.
        """
        if examination.tenant_id != tenant.id:
            raise ValidationError(
                {
                    "examination": (
                        "Examination does not belong "
                        "to the current tenant."
                    ),
                }
            )
        if examination.is_deleted:
            raise ValidationError(
                {
                    "examination": (
                        "Examination not found."
                    ),
                }
            )
        if (
            examination.status
            != ExaminationStatus.ACTIVE
        ):
            raise ValidationError(
                {
                    "examination": (
                        "Examination is inactive."
                    ),
                }
            )
        return examination
    @classmethod
    def _validate_obtained_marks(
        cls,
        examination: Examination,
        obtained_marks: int,
    ) -> None:
        """
        Validate obtained marks against the
        examination maximum marks.

        Args:
            examination:
                Examination instance.

            obtained_marks:
                Marks obtained by the student.

        Raises:
            ValidationError:
                If obtained marks exceed maximum marks.
        """

        if obtained_marks < 0:
            raise ValidationError(
                {
                    "obtained_marks": (
                        "Obtained marks cannot "
                        "be negative."
                    ),
                }
            )

        if (
            obtained_marks
            > examination.maximum_marks
        ):
            raise ValidationError(
                {
                    "obtained_marks": (
                        "Obtained marks cannot exceed "
                        "maximum marks."
                    ),
                }
            )

    @classmethod
    def _calculate_result_status(
        cls,
        examination: Examination,
        obtained_marks: int,
    ) -> ResultStatus:
        """
        Calculate PASS or FAIL based on the
        examination passing marks.

        Args:
            examination:
                Examination instance.

            obtained_marks:
                Marks obtained by the student.

        Returns:
            ResultStatus:
                PASS or FAIL.
        """

        if (
            obtained_marks
            >= examination.passing_marks
        ):
            return ResultStatus.PASS

        return ResultStatus.FAIL

    @classmethod
    def _check_duplicate_result(
        cls,
        tenant: Tenant,
        student: Student,
        examination: Examination,
        result_id: int | None = None,
    ) -> None:
        """
        Check whether a result already exists
        within the current tenant.

        Args:
            tenant:
                Current tenant.

            student:
                Student instance.

            examination:
                Examination instance.

            result_id:
                Current result ID during update.

        Raises:
            ValidationError:
                If a duplicate result exists
                within the tenant.
        """

        queryset = (
            Result.objects
            .for_tenant(tenant)
            .filter(
                student=student,
                examination=examination,
                is_deleted=False,
            )
        )

        if result_id is not None:
            queryset = queryset.exclude(
                id=result_id,
            )

        if queryset.exists():
            raise ValidationError(
                {
                    "result": (
                        "A result already exists "
                        "for this student and examination."
                    ),
                }
            )
# public methods
    @classmethod
    @transaction.atomic
    def create_result(
        cls,
        tenant,
        validated_data: dict,
    ) -> Result:
        """
        Create a new result within the current tenant.
        """

        student = cls._validate_student(
            tenant=tenant,
            student=validated_data["student"],
        )

        examination = cls._validate_examination(
            tenant=tenant,
            examination=validated_data["examination"],
        )

        cls._validate_obtained_marks(
            examination,
            validated_data["obtained_marks"],
        )

        cls._check_duplicate_result(
            tenant=tenant,
            student=student,
            examination=examination,
        )

        result_status = cls._calculate_result_status(
            examination,
            validated_data["obtained_marks"],
        )

        return (
            Result.objects
            .for_tenant(tenant)
            .create(
                student=student,
                examination=examination,
                obtained_marks=validated_data[
                    "obtained_marks"
                ],
                result_status=result_status,
                remarks=validated_data.get(
                    "remarks",
                    "",
                ),
            )
        )
    @classmethod
    def get_result_by_id(
        cls,
        tenant,
        result_id: int,
    ) -> Result:
        """
        Retrieve a result by its ID.

        Args:
            result_id (int):
                Result identifier.

        Returns:
            Result:
                Result instance.
        """
        return cls._get_result(
            tenant=tenant,
            result_id=result_id,
        )
    @classmethod
    def list_results(
        cls,
        tenant,
    ) -> QuerySet[Result]:
        """
        Retrieve all active results
        belonging to the current tenant.
        """

        return (
            Result.objects
            .for_tenant(tenant)
            .filter(
                is_deleted=False,
            )
            .select_related(
                "student",
                "student__user",
                "examination",
                "examination__subject",
            )
            .order_by(
                "-created_at",
            )
        )
    @classmethod
    @transaction.atomic
    def update_result(
        cls,
        tenant,
        result_id: int,
        validated_data: dict,
    ) -> Result:
        """
        Update an existing result within the current tenant.

        Args:
            tenant:
                Current tenant.

            result_id:
                Result identifier.

            validated_data:
                Validated serializer data.

        Returns:
            Result:
                Updated result instance.
        """

        result = cls._get_result(
            tenant=tenant,
            result_id=result_id,
        )

        student = cls._validate_student(
            tenant=tenant,
            student=validated_data["student"],
        )

        examination = cls._validate_examination(
            tenant=tenant,
            examination=validated_data["examination"],
        )

        cls._validate_obtained_marks(
            examination,
            validated_data["obtained_marks"],
        )

        cls._check_duplicate_result(
            tenant=tenant,
            student=student,
            examination=examination,
            result_id=result.id,
        )

        result.student = student
        result.examination = examination
        result.obtained_marks = validated_data[
            "obtained_marks"
        ]

        result.result_status = (
            cls._calculate_result_status(
                examination,
                validated_data["obtained_marks"],
            )
        )

        result.remarks = validated_data.get(
            "remarks",
            "",
        )

        result.save(
            update_fields=[
                "student",
                "examination",
                "obtained_marks",
                "result_status",
                "remarks",
                "updated_at",
            ],
        )

        return result
    @classmethod
    @transaction.atomic
    def change_result_status(
        cls,
        tenant,
        result_id: int,
        status: choices.ResultRecordStatus,
    ) -> Result:
        """
        Update the status of a result
        within the current tenant.

        Args:
            tenant:
                Current tenant.

            result_id:
                Result identifier.

            status:
                New result record status.

        Returns:
            Result:
                Updated result instance.
        """

        result = cls._get_result(
            tenant=tenant,
            result_id=result_id,
        )

        result.status = status

        result.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return result
    @classmethod
    @transaction.atomic
    def delete_result(
        cls,
        tenant,
        result_id: int,
    ) -> None:
        """
        Soft delete a result within the current tenant.

        Args:
            tenant:
                Current tenant.

            result_id:
                Result identifier.
        """

        result = cls._get_result(
            tenant=tenant,
            result_id=result_id,
        )

        result.is_deleted = True

        result.save(
            update_fields=[
                "is_deleted",
                "updated_at",
            ],
        )