"""
Serializers for examination write operations.
"""
from rest_framework import serializers
from apps.examinations.models import Examination
from .base import BaseExaminationSerializer
from rest_framework.validators import UniqueTogetherValidator

class ExaminationSerializer(BaseExaminationSerializer):
    """
    Serializer for examination list and detail responses.
    """
    class Meta(BaseExaminationSerializer.Meta):
        pass

class ExaminationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an examination.
    """
    class Meta:
        model = Examination
        fields = (
            "subject",
            "teacher",
            "exam_type",
            "semester",
            "academic_year",
            "exam_date",
            "maximum_marks",
            "passing_marks",
            "instructions",
        )

class ExaminationUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating an examination.
    """

    class Meta:
        model = Examination

        fields = (
            "subject",
            "teacher",
            "exam_type",
            "semester",
            "academic_year",
            "exam_date",
            "maximum_marks",
            "passing_marks",
            "instructions",
        )
class ExaminationStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for changing examination status.
    """

    class Meta:
        model = Examination

        fields = (
            "status",
        )
