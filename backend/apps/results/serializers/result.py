"""
Result serializers.

This module contains serializers used for
creating, updating, and representing results.
"""
from rest_framework import serializers
from apps.results.models import Result
from .base import BaseResultSerializer
class ResultCreateSerializer(BaseResultSerializer):
    """
    Serializer for creating a result.
    """
    class Meta(BaseResultSerializer.Meta):
        model = Result

        fields = (
            "student",
            "examination",
            "obtained_marks",
            "remarks",
        )
class ResultUpdateSerializer(BaseResultSerializer):
    """
    Serializer for updating a result.
    """
    class Meta(BaseResultSerializer.Meta):
        model = Result

        fields = (
            "student",
            "examination",
            "obtained_marks",
            "remarks",
        )
class ResultStatusSerializer(serializers.Serializer):
    """
    Serializer for updating result status.
    """
    status = serializers.ChoiceField(
        choices=Result._meta.get_field(
            "status"
        ).choices,
    )
class ResultSerializer(BaseResultSerializer):
    """
    Serializer for retrieving result details.
    """
    student_name = serializers.CharField(
        source="student.user.get_full_name",
        read_only=True,
    )
    class Meta(BaseResultSerializer.Meta):
        model = Result
        fields = BaseResultSerializer.Meta.fields + (
            "student_name",
        )