"""
Subject serializers.

This module defines serializers for subject-related
operations.
"""

from rest_framework import serializers

from apps.subjects.serializers.base import BaseSubjectSerializer


class SubjectCreateSerializer(BaseSubjectSerializer):
    """
    Serializer for creating a subject.
    """

    class Meta(BaseSubjectSerializer.Meta):
        """
        Metadata options for the subject creation serializer.
        """

        fields = (
            "course",
            "subject_name",
            "subject_code",
            "semester",
            "credits",
            "description",
        )


class SubjectUpdateSerializer(BaseSubjectSerializer):
    """
    Serializer for updating a subject.
    """

    class Meta(BaseSubjectSerializer.Meta):
        """
        Metadata options for the subject update serializer.
        """

        fields = (
            "course",
            "subject_name",
            "subject_code",
            "semester",
            "credits",
            "description",
        )

        extra_kwargs = {
            "course": {
                "required": False,
            },
            "subject_name": {
                "required": False,
            },
            "subject_code": {
                "required": False,
            },
            "semester": {
                "required": False,
            },
            "credits": {
                "required": False,
            },
            "description": {
                "required": False,
            },
        }


class SubjectSerializer(BaseSubjectSerializer):
    """
    Serializer for retrieving subject details.
    """

    class Meta(BaseSubjectSerializer.Meta):
        """
        Metadata options for the subject serializer.
        """

        fields = BaseSubjectSerializer.Meta.fields


class SubjectStatusSerializer(serializers.Serializer):
    """
    Serializer for updating subject status.
    """

    is_active = serializers.BooleanField()