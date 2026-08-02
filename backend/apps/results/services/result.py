"""
Business logic for result management.
"""
from django.core.exceptions import ValidationError
from apps.results.models import Result, choices
from apps.students.models import Student,choices
from apps.examinations.models import Examination, ExaminationStatus
from django.db.models import QuerySet
from django.db import transaction

class ResultService:
    """
    Service layer for managing results.
    """
    @classmethod
    def _get_result(
        cls,
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

        Raises:
            ValidationError:
                If the result does not exist.
        """

        try:
            return Result.objects.get(
                id=result_id,
                is_deleted=False,
            )

        except Result.DoesNotExist:
            raise ValidationError(
                "Result not found."
            )
    @classmethod
    def _validate_student(
        cls,
        student_id: int,
    ) -> Student:
        """
        Validate the student.

        Args:
            student_id (int):
                Student identifier.

        Returns:
            Student:
                Valid student instance.

        Raises:
            ValidationError:
                If the student does not exist or is inactive.
        """

        try:
            student = Student.objects.get(
                id=student_id,
                is_deleted=False,
            )

        except Student.DoesNotExist:
            raise ValidationError(
                "Student not found."
            )
        if student.status != choices.StudentStatus.ACTIVE:
            raise ValidationError(
                "Student is inactive."
            )

        return student
    @classmethod
    def _validate_examination(
        cls,
        examination_id: int,
    ) -> Examination:
        """
        Validate the examination.

        Args:
            examination_id (int):
                Examination identifier.

        Returns:
            Examination:
                Valid examination instance.

        Raises:
            ValidationError:
                If the examination does not exist or is inactive.
        """

        try:
            examination = Examination.objects.get(
                id=examination_id,
                is_deleted=False,
            )

        except Examination.DoesNotExist:
            raise ValidationError(
                "Examination not found."
            )

        if (
            examination.status
            != ExaminationStatus.ACTIVE
        ):
            raise ValidationError(
                "Examination is inactive."
            )

        return examination 
    @classmethod
    def _validate_obtained_marks(
        cls,
        examination: Examination,
        obtained_marks: int,
    ) -> None:
        """
        Validate obtained marks.

        Args:
            examination (Examination):
                Valid examination instance.

            obtained_marks (int):
                Marks obtained by the student.

        Raises:
            ValidationError:
                If obtained marks exceed the
                examination maximum marks.
        """

        if obtained_marks > examination.maximum_marks:
            raise ValidationError(
                "Obtained marks cannot exceed maximum marks."
            )
    @classmethod
    def _calculate_result_status(
        cls,
        examination: Examination,
        obtained_marks: int,
    ) -> choices.ResultStatus:
        """
        Calculate the student's result status.

        Args:
            examination (Examination):
                Valid examination instance.

            obtained_marks (int):
                Marks obtained by the student.

        Returns:
            ResultStatus:
                PASS or FAIL.
        """

        if obtained_marks >= examination.passing_marks:
            return choices.ResultStatus.PASS
        return choices.ResultStatus.FAIL
    
    @classmethod
    def _check_duplicate_result(
        cls,
        student: Student,
        examination: Examination,
        result_id: int | None = None,
    ) -> None:
        """
        Check whether a result already exists for the
        given student and examination.

        Args:
            student (Student):
                Valid student instance.

            examination (Examination):
                Valid examination instance.

            result_id (int | None):
                Current result identifier during update.

        Raises:
            ValidationError:
                If a duplicate result exists.
        """

        queryset = Result.objects.filter(
            student=student,
            examination=examination,
            is_deleted=False,
        )

        if result_id is not None:
            queryset = queryset.exclude(
                id=result_id,
            )

        if queryset.exists():
            raise ValidationError(
                "A result already exists for this student and examination."
            )
# public methods
    @classmethod
    @transaction.atomic
    def create_result(
        cls,
        validated_data: dict,
    ) -> Result:
        """
        Create a new result.

        Args:
            validated_data (dict):
                Validated serializer data.

        Returns:
            Result:
                Newly created result instance.
        """

        student = cls._validate_student(
            validated_data["student"]
        )

        examination = cls._validate_examination(
            validated_data["examination"]
        )

        cls._validate_obtained_marks(
            examination,
            validated_data["obtained_marks"],
        )

        cls._check_duplicate_result(
            student,
            examination,
        )

        result_status = cls._calculate_result_status(
            examination,
            validated_data["obtained_marks"],
        )

        return Result.objects.create(
            student=student,
            examination=examination,
            obtained_marks=validated_data["obtained_marks"],
            result_status=result_status,
            remarks=validated_data.get(
                "remarks",
                "",
            ),
        )
    @classmethod
    def get_result_by_id(
        cls,
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

        return cls._get_result(result_id)
    @classmethod
    def list_results(
        cls,
    ) -> QuerySet[Result]:
        """
        Retrieve all active results.

        Returns:
            QuerySet[Result]:
                Collection of result records.
        """

        return (
            Result.objects.filter(
                is_deleted=False,
            )
            .select_related(
                "student",
                "student__user",
                "examination",
                "examination__subject",
            )
        )
    @classmethod
    @transaction.atomic
    def update_result(
        cls,
        result_id: int,
        validated_data: dict,
    ) -> Result:
        """
        Update an existing result.

        Args:
            result_id (int):
                Result identifier.

            validated_data (dict):
                Validated serializer data.

        Returns:
            Result:
                Updated result instance.
        """

        result = cls._get_result(result_id)

        student = cls._validate_student(
            validated_data["student"]
        )

        examination = cls._validate_examination(
            validated_data["examination"]
        )

        cls._validate_obtained_marks(
            examination,
            validated_data["obtained_marks"],
        )

        cls._check_duplicate_result(
            student=student,
            examination=examination,
            result_id=result.id,
        )

        result.student = student
        result.examination = examination
        result.obtained_marks = validated_data["obtained_marks"]
        result.result_status = cls._calculate_result_status(
            examination,
            validated_data["obtained_marks"],
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
       ])

        return result
    @classmethod
    @transaction.atomic
    def change_result_status(
        cls,
        result_id: int,
        status: choices.ResultRecordStatus,
    ) -> Result:
        """
        Update the status of a result.

        Args:
            result_id (int):
                Result identifier.

            status (ResultRecordStatus):
                New result record status.

        Returns:
            Result:
                Updated result instance.
        """

        result = cls._get_result(result_id)

        result.status = status

        result.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return result
    @classmethod
    @transaction.atomic
    def delete_result(
        cls,
        result_id: int,
    ) -> None:
        """
        Soft delete a result.

        Args:
            result_id (int):
                Result identifier.
        """

        result = cls._get_result(result_id)

        result.is_deleted = True

        result.save(
            update_fields=[
                "is_deleted",
                "updated_at",
            ]
        )