"""
Subject API views.

This module contains API views for managing subjects.
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.core.permissions import IsAdminRole
from drf_spectacular.utils import extend_schema
from apps.subjects.serializers import (
    SubjectCreateSerializer,
    SubjectSerializer,
    SubjectStatusSerializer,
    SubjectUpdateSerializer,
)
from apps.subjects.services import SubjectService


class SubjectAPIView(APIView):
    """
    API view for creating, retrieving, and updating subjects.
    """

    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]
    @extend_schema(
    request=SubjectCreateSerializer,
    responses=SubjectSerializer,
)
    def post(self, request):
        """
        Create a new subject.
        """

        serializer = SubjectCreateSerializer(
            data=request.data,
            context={
                "tenant": request.tenant,
            },
        )

        serializer.is_valid(
            raise_exception=True,
        )

        subject = SubjectService.create_subject(
            tenant=request.tenant,
            validated_data=serializer.validated_data,
        )

        response_serializer = SubjectSerializer(
            subject,
            context={
                "tenant": request.tenant,
            },
        )

        return Response(
            {
                "message": "Subject created successfully.",
                "data": response_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def get(self, request, subject_id: int):
        """
        Retrieve a subject by ID.
        """

        subject = SubjectService.get_subject_by_id(
            tenant=request.tenant,
            subject_id=subject_id,
        )

        serializer = SubjectSerializer(
            subject,
            context={
                "tenant": request.tenant,
            },
        )

        return Response(
            {
                "message": "Subject retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    @extend_schema(
        request=SubjectUpdateSerializer,
        responses=SubjectSerializer,
    )
    def put(self, request, subject_id: int):
        """
        Update an existing subject.
        """

        serializer = SubjectUpdateSerializer(
            data=request.data,
            partial=True,
            context={
                "tenant": request.tenant,
            },
        )

        serializer.is_valid(
            raise_exception=True,
        )

        subject = SubjectService.update_subject(
            tenant=request.tenant,
            subject_id=subject_id,
            validated_data=serializer.validated_data,
        )

        response_serializer = SubjectSerializer(
            subject,
            context={
                "tenant": request.tenant,
            },
        )

        return Response(
            {
                "message": "Subject updated successfully.",
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class SubjectListAPIView(APIView):
    """
    API view for listing subjects.
    """

    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]

    def get(self, request):
        """
        Retrieve all subjects for the current tenant.
        """

        subjects = SubjectService.list_subjects(
            tenant=request.tenant,
        )

        serializer = SubjectSerializer(
            subjects,
            many=True,
            context={
                "tenant": request.tenant,
            },
        )

        return Response(
            {
                "message": "Subjects retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
class SubjectStatusAPIView(APIView):
    """
    API view for changing subject status.
    """

    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]
    @extend_schema(
        request=SubjectStatusSerializer,
        responses=SubjectSerializer,
    )
    def patch(self, request, subject_id: int):
        """
        Activate or deactivate a subject.
        """

        serializer = SubjectStatusSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        subject = SubjectService.change_subject_status(
            tenant=request.tenant,
            subject_id=subject_id,
            is_active=serializer.validated_data["is_active"],
        )

        response_serializer = SubjectSerializer(
            subject,
            context={
                "tenant": request.tenant,
            },
        )

        return Response(
            {
                "message": "Subject status updated successfully.",
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class SubjectDeleteAPIView(APIView):
    """
    API view for soft deleting a subject.
    """

    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]

    def delete(self, request, subject_id: int):
        """
        Soft delete a subject.
        """

        SubjectService.delete_subject(
            tenant=request.tenant,
            subject_id=subject_id,
        )

        return Response(
            {
                "message": "Subject deleted successfully.",
            },
            status=status.HTTP_204_NO_CONTENT,
        )
