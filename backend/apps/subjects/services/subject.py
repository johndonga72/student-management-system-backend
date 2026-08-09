"""
Subject service.

This module contains the business logic for managing
subjects.
"""
from __future__ import annotations
from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError
from apps.courses.models import Course
from apps.subjects.models import Subject
class SubjectService:
    """
    Service class for subject-related business operations.
    """
    # ==========================================================
    # Private Helper Methods
    # ==========================================================
    @staticmethod
    def _get_subject(
        *,
        tenant,
        subject_id: int,
    ) -> Subject:
        """
        Retrieve a subject by its ID within the current tenant.

        Args:
            tenant:
                Current tenant.

            subject_id:
                Primary key of the subject.

        Returns:
            Subject:
                Subject instance.

        Raises:
            Http404:
                If the subject does not exist within the tenant.
        """

        return get_object_or_404(
            Subject.objects.for_tenant(
                tenant,
            ).select_related(
                "course",
            ),
            pk=subject_id,
            is_deleted=False,
        )

    @staticmethod
    def _validate_course(
        *,
        tenant,
        course: Course,
    ) -> None:
        """
        Validate whether the course can be assigned
        to a subject within the current tenant.

        Args:
            tenant:
                Current tenant.

            course:
                Course instance.

        Raises:
            ValidationError:
                If the course does not belong to the tenant,
                is inactive, or is deleted.
        """

        if course.tenant_id != tenant.id:
            raise ValidationError(
                "Selected course does not belong to this tenant."
            )

        if course.is_deleted:
            raise ValidationError(
                "Cannot assign a deleted course."
            )

        if not course.is_active:
            raise ValidationError(
                "Cannot assign an inactive course."
            )

    @staticmethod
    def _subject_name_exists(
        *,
        tenant,
        course: Course,
        subject_name: str,
        exclude_id: int | None = None,
    ) -> bool:
        """
        Check whether a subject name already exists
        within a course and tenant.

        Args:
            tenant:
                Current tenant.

            course:
                Course instance.

            subject_name:
                Subject name.

            exclude_id:
                Subject ID excluded during updates.

        Returns:
            bool:
                True if the subject name already exists.
        """

        queryset = (
            Subject.objects
            .for_tenant(tenant)
            .filter(
                course=course,
                subject_name__iexact=subject_name.strip(),
                is_deleted=False,
            )
        )

        if exclude_id is not None:
            queryset = queryset.exclude(
                pk=exclude_id,
            )

        return queryset.exists()

    @staticmethod
    def _subject_code_exists(
        *,
        tenant,
        course: Course,
        subject_code: str,
        exclude_id: int | None = None,
    ) -> bool:
        """
        Check whether a subject code already exists
        within a course and tenant.

        Args:
            tenant:
                Current tenant.

            course:
                Course instance.

            subject_code:
                Subject code.

            exclude_id:
                Subject ID excluded during updates.

        Returns:
            bool:
                True if the subject code already exists.
        """

        queryset = (
            Subject.objects
            .for_tenant(tenant)
            .filter(
                course=course,
                subject_code__iexact=subject_code.strip(),
                is_deleted=False,
            )
        )

        if exclude_id is not None:
            queryset = queryset.exclude(
                pk=exclude_id,
            )

        return queryset.exists()

    @staticmethod
    def _validate_semester(
        semester: int,
    ) -> None:
        """
        Validate semester.

        Args:
            semester:
                Semester number.

        Raises:
            ValidationError:
                If the semester is outside the allowed range.
        """

        if not 1 <= semester <= 8:
            raise ValidationError(
                "Semester must be between 1 and 8."
            )

    @staticmethod
    def _validate_credits(
        credits: int,
    ) -> None:
        """
        Validate subject credits.

        Args:
            credits:
                Number of credits.

        Raises:
            ValidationError:
                If credits are outside the allowed range.
        """

        if not 1 <= credits <= 6:
            raise ValidationError(
                "Credits must be between 1 and 6."
            )
    # ==========================================================
    # Public Business Methods
    # ==========================================================
    @staticmethod
    def create_subject(
        *,
        tenant,
        validated_data: dict,
    ) -> Subject:
        """
        Create a new subject for the current tenant.

        Args:
            tenant:
                Current tenant.

            validated_data:
                Validated subject data.

        Returns:
            Subject:
                Newly created subject.

        Raises:
            ValidationError:
                If the subject violates business rules.
        """

        # ---------------------------------------------------------
        # Extract validated data
        # ---------------------------------------------------------

        course = validated_data["course"]
        subject_name = validated_data["subject_name"]
        subject_code = validated_data["subject_code"]

        # ---------------------------------------------------------
        # Validate business rules
        # ---------------------------------------------------------

        SubjectService._validate_course(
            tenant=tenant,
            course=course,
        )

        if SubjectService._subject_name_exists(
            tenant=tenant,
            course=course,
            subject_name=subject_name,
        ):
            raise ValidationError(
                "Subject name already exists for this course."
            )

        if SubjectService._subject_code_exists(
            tenant=tenant,
            course=course,
            subject_code=subject_code,
        ):
            raise ValidationError(
                "Subject code already exists for this course."
            )

        # ---------------------------------------------------------
        # Create subject
        # ---------------------------------------------------------

        return Subject.objects.create(
            tenant=tenant,
            **validated_data,
        )


    @staticmethod
    def get_subject_by_id(
        *,
        tenant,
        subject_id: int,
    ) -> Subject:
        """
        Retrieve a subject by its ID within the current tenant.

        Args:
            tenant:
                Current tenant.

            subject_id:
                Subject primary key.

        Returns:
            Subject:
                Subject instance.
        """

        return SubjectService._get_subject(
            tenant=tenant,
            subject_id=subject_id,
        )


    @staticmethod
    def list_subjects(
        *,
        tenant,
    ) -> QuerySet[Subject]:
        """
        Retrieve all available subjects
        belonging to the current tenant.

        Args:
            tenant:
                Current tenant.

        Returns:
            QuerySet[Subject]:
                Collection of tenant-scoped subjects.
        """

        return (
            Subject.objects
            .for_tenant(tenant)
            .select_related(
                "course",
            )
            .filter(
                is_deleted=False,
            )
            .order_by(
                "semester",
                "subject_name",
            )
        )


    @staticmethod
    def update_subject(
        *,
        tenant,
        subject_id: int,
        validated_data: dict,
    ) -> Subject:
        """
        Update an existing subject within the current tenant.

        Args:
            tenant:
                Current tenant.

            subject_id:
                Subject primary key.

            validated_data:
                Validated update data.

        Returns:
            Subject:
                Updated subject.
        """

        # ---------------------------------------------------------
        # Retrieve subject
        # ---------------------------------------------------------

        subject = SubjectService._get_subject(
            tenant=tenant,
            subject_id=subject_id,
        )

        # ---------------------------------------------------------
        # Resolve updated values
        # ---------------------------------------------------------

        course = validated_data.get(
            "course",
            subject.course,
        )

        subject_name = validated_data.get(
            "subject_name",
            subject.subject_name,
        )

        subject_code = validated_data.get(
            "subject_code",
            subject.subject_code,
        )

        # ---------------------------------------------------------
        # Validate business rules
        # ---------------------------------------------------------

        SubjectService._validate_course(
            tenant=tenant,
            course=course,
        )

        if SubjectService._subject_name_exists(
            tenant=tenant,
            course=course,
            subject_name=subject_name,
            exclude_id=subject.id,
        ):
            raise ValidationError(
                "Subject name already exists for this course."
            )

        if SubjectService._subject_code_exists(
            tenant=tenant,
            course=course,
            subject_code=subject_code,
            exclude_id=subject.id,
        ):
            raise ValidationError(
                "Subject code already exists for this course."
            )

        # ---------------------------------------------------------
        # Update fields
        # ---------------------------------------------------------

        for field, value in validated_data.items():
            setattr(
                subject,
                field,
                value,
            )

        subject.save()

        return subject

    @staticmethod
    def change_subject_status(
        *,
        tenant,
        subject_id: int,
        is_active: bool,
    ) -> Subject:
        """
        Activate or deactivate a subject
        within the current tenant.
        """

        subject = SubjectService._get_subject(
            tenant=tenant,
            subject_id=subject_id,
        )

        subject.is_active = is_active

        subject.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        return subject


    @staticmethod
    def delete_subject(
        *,
        tenant,
        subject_id: int,
    ) -> None:
        """
        Soft delete a subject within the current tenant.
        """

        subject = SubjectService._get_subject(
            tenant=tenant,
            subject_id=subject_id,
        )

        subject.is_deleted = True

        subject.save(
            update_fields=[
                "is_deleted",
                "updated_at",
            ]
        )
