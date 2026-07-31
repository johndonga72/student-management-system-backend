"""
Base serializers for the Examination module.
"""

from rest_framework import serializers

from apps.examinations.models import Examination


class BaseExaminationSerializer(serializers.ModelSerializer):
    """
    Base serializer for examination details.
    """

    subject_name = serializers.CharField(
        source="subject.subject_name",
        read_only=True,
    )

    teacher_email = serializers.EmailField(
        source="teacher.user.email",
        read_only=True,
    )

    teacher_employee_id = serializers.CharField(
        source="teacher.employee_id",
        read_only=True,
    )

    exam_type_display = serializers.CharField(
        source="get_exam_type_display",
        read_only=True,
    )

    semester_display = serializers.CharField(
        source="get_semester_display",
        read_only=True,
    )

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = Examination

        fields = (
            "id",

            # Subject
            "subject",
            "subject_name",

            # Teacher
            "teacher",
            "teacher_email",
            "teacher_employee_id",

            # Examination
            "exam_type",
            "exam_type_display",
            "semester",
            "semester_display",
            "academic_year",
            "exam_date",

            # Marks
            "maximum_marks",
            "passing_marks",

            # Additional Information
            "instructions",
            "status",
            "status_display",

            # Audit
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "subject_name",
            "teacher_email",
            "teacher_employee_id",
            "exam_type_display",
            "semester_display",
            "status_display",
            "created_at",
            "updated_at",
        )