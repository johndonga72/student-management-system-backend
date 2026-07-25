"""
Base serializer for the Subject model.

This module defines the reusable serializer for the
Subject model. It serves as the foundation for all
subject-related serializers.
"""

from rest_framework import serializers

from apps.subjects.models import Subject


class BaseSubjectSerializer(serializers.ModelSerializer):
    """
    Base serializer for the Subject model.
    """

    class Meta:
        """
        Metadata options for the base subject serializer.
        """

        model = Subject

        fields = (
            "id",
            "course",
            "subject_name",
            "subject_code",
            "semester",
            "credits",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )