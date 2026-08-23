from apps.examinations.models import Examination
from apps.teachers.models import Teacher
from apps.subjects.models import Subject
from rest_framework.exceptions import ValidationError
from django.db.models import QuerySet
from django.db import transaction
from apps.tenants.models import Tenant
class ExaminationService:
    """
    Service class for Examination business logic.
    """
    @classmethod
    def _get_examination(
        cls,
        tenant: Tenant,
        examination_id: int,
    ) -> Examination:
        """
        Retrieve an examination belonging to the current tenant.

        Args:
            tenant: Current tenant.
            examination_id: Examination ID.

        Returns:
            Examination: Matching examination.

        Raises:
            ValidationError: If the examination does not exist
                within the current tenant.
        """

        try:
            return (
                Examination.objects
                .for_tenant(tenant)
                .select_related(
                    "subject",
                    "teacher__user",
                )
                .get(
                    id=examination_id,
                    is_deleted=False,
                )
            )

        except Examination.DoesNotExist as exc:
            raise ValidationError(
                {
                    "examination": (
                        "Examination does not exist."
                    ),
                }
            ) from exc

    @classmethod
    def _validate_teacher(
        cls,
        tenant: Tenant,
        teacher_id: int,
    ) -> Teacher:
        """
        Validate that the teacher belongs to
        the current tenant.
        """

        try:
            return (
                Teacher.objects
                .for_tenant(tenant)
                .select_related(
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
                        "Teacher does not exist "
                        "for the current tenant."
                    ),
                }
            ) from exc

    @classmethod
    def _validate_subject(
        cls,
        tenant: Tenant,
        subject_id: int,
    ) -> Subject:
        """
        Validate that the subject belongs to
        the current tenant.
        """

        try:
            return (
                Subject.objects
                .for_tenant(tenant)
                .select_related(
                    "course__department",
                )
                .get(
                    id=subject_id,
                    is_deleted=False,
                )
            )

        except Subject.DoesNotExist as exc:
            raise ValidationError(
                {
                    "subject": (
                        "Subject does not exist "
                        "for the current tenant."
                    ),
                }
            ) from exc

    @classmethod
    def _validate_teacher_subject(
        cls,
        teacher: Teacher,
        subject: Subject,
    ) -> None:
        """
        Validate that the teacher is assigned
        to the selected subject.
        """

        if not teacher.subjects.filter(
            id=subject.id,
        ).exists():
            raise ValidationError(
                {
                    "subject": (
                        "The selected teacher is not "
                        "assigned to this subject."
                    ),
                }
            )

    @classmethod
    def _validate_maximum_marks(
        cls,
        maximum_marks: int,
    ) -> None:
        """
        Validate maximum examination marks.
        """

        if maximum_marks <= 0:
            raise ValidationError(
                {
                    "maximum_marks": (
                        "Maximum marks must be "
                        "greater than zero."
                    ),
                }
            )

    @classmethod
    def _validate_passing_marks(
        cls,
        maximum_marks: int,
        passing_marks: int,
    ) -> None:
        """
        Validate passing marks.
        """

        if passing_marks < 0:
            raise ValidationError(
                {
                    "passing_marks": (
                        "Passing marks cannot "
                        "be negative."
                    ),
                }
            )

        if passing_marks > maximum_marks:
            raise ValidationError(
                {
                    "passing_marks": (
                        "Passing marks cannot exceed "
                        "maximum marks."
                    ),
                }
            )

    @classmethod
    def _validate_exam_date(
        cls,
        exam_date,
    ) -> None:
        """
        Validate the examination date.
        """

        if exam_date is None:
            raise ValidationError(
                {
                    "exam_date": (
                        "Examination date is required."
                    ),
                }
            )

    @classmethod
    def _check_duplicate_examination(
        cls,
        tenant: Tenant,
        *,
        subject: Subject,
        exam_type,
        semester,
        academic_year: str,
        exclude_id: int = None,
    ) -> None:
        """
        Check for duplicate examination
        within the current tenant only.
        """

        queryset = (
            Examination.objects
            .for_tenant(tenant)
            .filter(
                subject=subject,
                exam_type=exam_type,
                semester=semester,
                academic_year=academic_year,
                is_deleted=False,
            )
        )

        if exclude_id is not None:
            queryset = queryset.exclude(
                id=exclude_id,
            )

        if queryset.exists():
            raise ValidationError(
                {
                    "examination": (
                        "An examination with the same "
                        "subject, exam type, semester, "
                        "and academic year already exists "
                        "for this tenant."
                    ),
                }
            )
# ==========================================================
# Public Methods
# ==========================================================

    @classmethod
    @transaction.atomic
    def create_examination(
        cls,
        tenant: Tenant,
        validated_data: dict,
    ) -> Examination:
        """
        Create a new examination for the current tenant.
        """

        teacher = cls._validate_teacher(
            tenant=tenant,
            teacher_id=validated_data["teacher"].id,
        )

        subject = cls._validate_subject(
            tenant=tenant,
            subject_id=validated_data["subject"].id,
        )

        cls._validate_teacher_subject(
            teacher=teacher,
            subject=subject,
        )

        cls._validate_maximum_marks(
            validated_data["maximum_marks"],
        )

        cls._validate_passing_marks(
            validated_data["maximum_marks"],
            validated_data["passing_marks"],
        )

        cls._validate_exam_date(
            validated_data["exam_date"],
        )

        cls._check_duplicate_examination(
            tenant=tenant,
            subject=subject,
            exam_type=validated_data["exam_type"],
            semester=validated_data["semester"],
            academic_year=validated_data["academic_year"],
        )

        examination = Examination.objects.create(
            tenant=tenant,
            **validated_data,
        )

        return examination


    @classmethod
    def get_examination_by_id(
        cls,
        tenant: Tenant,
        examination_id: int,
    ) -> Examination:
        """
        Retrieve an examination belonging to
        the current tenant.
        """

        return cls._get_examination(
            tenant=tenant,
            examination_id=examination_id,
        )


    @classmethod
    def list_examinations(
        cls,
        tenant: Tenant,
    ) -> QuerySet[Examination]:
        """
        Retrieve all examinations belonging to
        the current tenant.
        """

        return (
            Examination.objects
            .for_tenant(tenant)
            .select_related(
                "subject",
                "teacher__user",
            )
            .filter(
                is_deleted=False,
            )
            .order_by(
                "exam_date",
            )
        )
    @classmethod
    @transaction.atomic
    def update_examination(
        cls,
        tenant: Tenant,
        examination_id: int,
        validated_data: dict,
    ) -> Examination:
        """
        Update an existing examination belonging to
        the current tenant.

        Args:
            tenant: Current tenant.
            examination_id: Examination ID.
            validated_data: Validated examination data.

        Returns:
            Examination: Updated examination.
        """

        examination = cls._get_examination(
            tenant=tenant,
            examination_id=examination_id,
        )

        teacher = cls._validate_teacher(
            tenant=tenant,
            teacher_id=validated_data["teacher"].id,
        )

        subject = cls._validate_subject(
            tenant=tenant,
            subject_id=validated_data["subject"].id,
        )

        cls._validate_teacher_subject(
            teacher=teacher,
            subject=subject,
        )

        cls._validate_maximum_marks(
            validated_data["maximum_marks"],
        )

        cls._validate_passing_marks(
            validated_data["maximum_marks"],
            validated_data["passing_marks"],
        )

        cls._validate_exam_date(
            validated_data["exam_date"],
        )

        cls._check_duplicate_examination(
            tenant=tenant,
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
    @transaction.atomic
    def change_examination_status(
        cls,
        tenant: Tenant,
        examination_id: int,
        status: str,
    ) -> Examination:
        """
        Change examination status for the current tenant.

        Args:
            tenant: Current tenant.
            examination_id: Examination ID.
            status: New examination status.

        Returns:
            Examination: Updated examination.
        """

        examination = cls._get_examination(
            tenant=tenant,
            examination_id=examination_id,
        )

        examination.status = status

        examination.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return examination
    @classmethod
    @transaction.atomic
    def delete_examination(
        cls,
        tenant: Tenant,
        examination_id: int,
    ) -> Examination:
        """
        Soft delete an examination belonging to
        the current tenant.

        Args:
            tenant: Current tenant.
            examination_id: Examination ID.

        Returns:
            Examination: Soft-deleted examination.
        """

        examination = cls._get_examination(
            tenant=tenant,
            examination_id=examination_id,
        )

        examination.is_deleted = True

        examination.save(
            update_fields=[
                "is_deleted",
                "updated_at",
            ],
        )

        return examination