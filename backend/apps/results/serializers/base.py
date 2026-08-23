"""
Base serializer for the Result module.
"""

from rest_framework import serializers

from apps.results.models import Result

class BaseResultSerializer(serializers.ModelSerializer):
    """
    Base serializer for representing result information.
    """

    exam_type = serializers.CharField(
        source="examination.exam_type",
        read_only=True,
    )

    exam_date = serializers.DateField(
        source="examination.exam_date",
        read_only=True,
    )

    academic_year = serializers.CharField(
        source="examination.academic_year",
        read_only=True,
    )

    subject_name = serializers.CharField(
        source="examination.subject.subject_name",
        read_only=True,
    )

    student_number = serializers.CharField(
        source="student.student_number",
        read_only=True,
    )

    class Meta:
        model = Result

        fields = (
            "id",
            "student",
            "student_number",
            "examination",
            "subject_name",
            "exam_type",
            "exam_date",
            "academic_year",
            "obtained_marks",
            "result_status",
            "remarks",
            "status",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "student_number",
            "subject_name",
            "exam_type",
            "exam_date",
            "academic_year",
            "result_status",
            "created_at",
            "updated_at",
        )