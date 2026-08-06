from apps.examinations.models import Examination
from apps.teachers.models import Teacher
from apps.subjects.models import Subject
from rest_framework.exceptions import ValidationError
from django.db.models import QuerySet
from django.db import transaction
class ExaminationService:
    """
    Service class for Examination business logic.
    """
# Private methods
    @classmethod
    def _get_examination(cls, examination_id: int) -> Examination:
        """
        Retrieve an examination by ID.

        Raises:
            ExaminationNotFoundException:
                If the examination does not exist.
        """

        try:
            return (
                Examination.objects
                .select_related(
                    "subject",
                    "teacher__user",
                )
                .get(
                    id=examination_id,
                    is_deleted=False,
                )
            )

        except Examination.DoesNotExist:
            raise ValidationError(
          "exam doesnot found."
    )
    @classmethod
    def _validate_teacher(cls, teacher_id: int) -> Teacher:
        """
        Validate that the teacher exists.

        Args:
            teacher_id: Teacher ID.

        Returns:
            Teacher object.

        Raises:
            ValidationError:
                If the teacher does not exist.
        """

        try:
            return Teacher.objects.select_related(
                "user",
                "department",
            ).get(
                id=teacher_id,
                is_deleted=False,
            )

        except Teacher.DoesNotExist:
            raise ValidationError(
                "Teacher not found."
            )
    @classmethod
    def _validate_subject(cls, subject_id: int) -> Subject:
        """
        Validate that the subject exists.

        Args:
            subject_id: Subject ID.

        Returns:
            Subject object.

        Raises:
            ValidationError:
                If the subject does not exist.
        """

        try:
            return Subject.objects.select_related(
                "course__department",
            ).get(
                id=subject_id,
                is_deleted=False,
            )

        except Subject.DoesNotExist:
            raise ValidationError(
                "Subject not found."
            )

    @classmethod
    def _validate_teacher_subject(
        cls,
        teacher: Teacher,
        subject: Subject,
    ) -> None:
        """
        Validate that the teacher is assigned to the selected subject.

        Args:
            teacher: Teacher instance.
            subject: Subject instance.

        Raises:
            ValidationError:
                If the teacher is not assigned to the subject.
        """

        if not teacher.subjects.filter(id=subject.id).exists():
            raise ValidationError(
                "The selected teacher is not assigned to this subject."
            )
    @classmethod
    def _validate_maximum_marks(
        cls,
        maximum_marks: int,
    ) -> None:
        """
        Validate maximum marks.

        Args:
            maximum_marks: Maximum marks for the examination.

        Raises:
            ValidationError:
                If maximum marks are less than or equal to zero.
        """

        if maximum_marks <= 0:
            raise ValidationError(
                "Maximum marks must be greater than zero."
            )
    @classmethod
    def _validate_passing_marks(
        cls,
        maximum_marks: int,
        passing_marks: int,
    ) -> None:
        """
        Validate passing marks.

        Args:
            maximum_marks: Maximum marks for the examination.
            passing_marks: Passing marks for the examination.

        Raises:
            ValidationError:
                If passing marks are invalid.
        """

        if passing_marks < 0:
            raise ValidationError(
                "Passing marks cannot be negative."
            )

        if passing_marks > maximum_marks:
            raise ValidationError(
                "Passing marks cannot exceed maximum marks."
            )
    @classmethod
    def _validate_exam_date(
        cls,
        exam_date,
    ) -> None:
        """
        Validate the examination date.

        Args:
            exam_date: Examination date.

        Raises:
            ValidationError:
                If the examination date is not provided.
        """

        if exam_date is None:
            raise ValidationError(
                "Examination date is required."
            )
    @classmethod
    def _check_duplicate_examination(
        cls,
        *,
        subject,
        exam_type,
        semester,
        academic_year,
        exclude_id: int = None,
    ) -> None:
        """
        Validate that the examination does not already exist.

        Args:
            subject: Subject instance.
            exam_type: Examination type.
            semester: Semester.
            academic_year: Academic year.
            exclude_id: Examination ID to exclude during update.

        Raises:
            ValidationError:
                If a duplicate examination already exists.
        """

        queryset = Examination.objects.filter(
            subject=subject,
            exam_type=exam_type,
            semester=semester,
            academic_year=academic_year,
            is_deleted=False,
        )

        if exclude_id:
            queryset = queryset.exclude(id=exclude_id)

        if queryset.exists():
            raise ValidationError(
                "An examination with the same subject, exam type, semester, and academic year already exists."
            )
# Public methods
    @classmethod
    def create_examination(cls, validated_data: dict) -> Examination:
        """
        Create a new examination.
        """

        with transaction.atomic():

            teacher = cls._validate_teacher(
                validated_data["teacher"].id
            )

            subject = cls._validate_subject(
                validated_data["subject"].id
            )

            cls._validate_teacher_subject(
                teacher,
                subject,
            )

            cls._validate_maximum_marks(
                validated_data["maximum_marks"]
            )

            cls._validate_passing_marks(
                validated_data["maximum_marks"],
                validated_data["passing_marks"],
            )

            cls._validate_exam_date(
                validated_data["exam_date"]
            )

            cls._check_duplicate_examination(
                subject=subject,
                exam_type=validated_data["exam_type"],
                semester=validated_data["semester"],
                academic_year=validated_data["academic_year"],
            )

            examination = Examination.objects.create(
                **validated_data
            )

            return examination
    @classmethod
    def get_examination_by_id(
        cls,
        examination_id: int,
    ) -> Examination:
        """
        Retrieve an examination by ID.

        Args:
            examination_id: Examination ID.

        Returns:
            Examination object.
        """

        return cls._get_examination(
            examination_id
        )   
    @classmethod
    def list_examinations(cls) -> QuerySet[Examination]:
        """
        Retrieve all examinations.

        Returns:
            QuerySet[Examination]: List of examinations.
        """

        return (
            Examination.objects
            .select_related(
                "subject",
                "teacher__user",
            )
            .filter(
                is_deleted=False,
            )
            .order_by("exam_date")
        )
    @classmethod
    def update_examination(
        cls,
        examination_id: int,
        validated_data: dict,
    ) -> Examination:
        """
        Update an existing examination.
        """

        with transaction.atomic():

            examination = cls._get_examination(
                examination_id
            )

            teacher = cls._validate_teacher(
                validated_data["teacher"].id
            )

            subject = cls._validate_subject(
                validated_data["subject"].id
            )

            cls._validate_teacher_subject(
                teacher,
                subject,
            )

            cls._validate_maximum_marks(
                validated_data["maximum_marks"]
            )

            cls._validate_passing_marks(
                validated_data["maximum_marks"],
                validated_data["passing_marks"],
            )

            cls._validate_exam_date(
                validated_data["exam_date"]
            )

            cls._check_duplicate_examination(
                subject=subject,
                exam_type=validated_data["exam_type"],
                semester=validated_data["semester"],
                academic_year=validated_data["academic_year"],
                exclude_id=examination.id,
            )

            for field, value in validated_data.items():
                setattr(
                    examination,
                    field,
                    value,
                )

            examination.save()

            return examination
    @classmethod
    def change_examination_status(
        cls,
        examination_id: int,
        status: str,
    ) -> Examination:
        """
        Change examination status.
        """

        with transaction.atomic():

            examination = cls._get_examination(
                examination_id
            )

            examination.status = status
            examination.save(
                update_fields=["status"]
            )

            return examination
    @classmethod
    def delete_examination(
        cls,
        examination_id: int,
    ) -> Examination:
        """
        Soft delete an examination.
        """

        with transaction.atomic():

            examination = cls._get_examination(
                examination_id
            )

            examination.is_deleted = True

            examination.save(
                update_fields=["is_deleted"]
            )
        return examination