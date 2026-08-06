from rest_framework import serializers
from apps.results.models import Result
from .base import BaseResultSerializer
from rest_framework.validators import UniqueTogetherValidator
class ResultCreateSerializer(BaseResultSerializer):
    """
    Serializer for creating a result.
    """
    class Meta(BaseResultSerializer.Meta):
        fields = [
            "student",
            "examination",
            "obtained_marks",
            "remarks",
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Result.objects.filter(
                    is_deleted=False,
                ),
                fields=(
                    "student",
                    "examination",
                ),
                message=(
                    "A result for this student and examination "
                    "already exists."
                ),
            ),
        ]
class ResultUpdateSerializer(BaseResultSerializer):
    """
    Serializer for updating a result.
    """

    class Meta(BaseResultSerializer.Meta):
        fields = [
            "student",
            "examination",
            "obtained_marks",
            "remarks",
        ]
class ResultStatusSerializer(serializers.Serializer):
    """
    Serializer for updating result status.
    """
    status = serializers.ChoiceField(
        choices=Result._meta.get_field(
            "status"
        ).choices
    )
class ResultSerializer(BaseResultSerializer):
    """
    Serializer for retrieving result details.
    """
    student_name = serializers.CharField(
        source="student.user.full_name",
        read_only=True,
    )
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
    class Meta(BaseResultSerializer.Meta):
        fields = BaseResultSerializer.Meta.fields + [
            "student_name",
            "exam_type",
            "subject_name",
        ]