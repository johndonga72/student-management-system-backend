"""
Teacher API views.

This module contains API views for managing
teacher operations.
"""
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.core.permissions import IsAdminRole
from apps.teachers.serializers import (
    TeacherCreateSerializer,
    TeacherSerializer,
    TeacherStatusSerializer,
    TeacherUpdateSerializer,
)
from apps.teachers.services import TeacherService

class TeacherAPIView(APIView):
    """
    API view for managing teacher operations.
    """

    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]

    @staticmethod
    def get_service() -> TeacherService:
        """
        Return the teacher service.
        """
        return TeacherService
    
    @extend_schema(
    request=TeacherCreateSerializer,
    responses=TeacherSerializer,
)
    def post(
        self,
        request,
    ):
        """
        Create a teacher profile
        within the current tenant.
        """
        serializer = TeacherCreateSerializer(
            data=request.data,
            context={
                "tenant": request.tenant,
            },
        )
        serializer.is_valid(
            raise_exception=True,
        )
        service = self.get_service()

        teacher = service.create_teacher(
            tenant=request.tenant,
            validated_data=serializer.validated_data,
        )

        response_serializer = TeacherSerializer(
            teacher,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def get(
        self,
        request,
        teacher_id: int = None,
    ):
        """
        Retrieve teacher information
        within the current tenant.
        """

        service = self.get_service()

        # ---------------------------------------------
        # List teachers
        # ---------------------------------------------

        if teacher_id is None:

            teachers = service.list_teachers(
                tenant=request.tenant,
            )

            serializer = TeacherSerializer(
                teachers,
                many=True,
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        # ---------------------------------------------
        # Retrieve teacher
        # ---------------------------------------------

        teacher = service.get_teacher_by_id(
            tenant=request.tenant,
            teacher_id=teacher_id,
        )

        serializer = TeacherSerializer(
            teacher,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    @extend_schema(
        request=TeacherUpdateSerializer,
        responses=TeacherSerializer,
    )
    def put(
        self,
        request,
        teacher_id: int,
    ):
        """
        Update a teacher profile
        within the current tenant.
        """

        serializer = TeacherUpdateSerializer(
            data=request.data,
            partial=True,
            context={
                "tenant": request.tenant,
            },
        )

        serializer.is_valid(
            raise_exception=True,
        )

        teacher = self.get_service().update_teacher(
            tenant=request.tenant,
            teacher_id=teacher_id,
            validated_data=serializer.validated_data,
        )

        response_serializer = TeacherSerializer(
            teacher,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )
class TeacherListAPIView(APIView):
    """
    API view for listing teacher profiles.
    """

    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]

    @staticmethod
    def get_service() -> TeacherService:
        """
        Return the teacher service.
        """
        return TeacherService

    def get(
        self,
        request,
    ):
        """
        Retrieve all teacher profiles
        for the current tenant.
        """

        service = self.get_service()

        teachers = service.list_teachers(
            tenant=request.tenant,
        )

        serializer = TeacherSerializer(
            teachers,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
class TeacherStatusAPIView(APIView):
    """
    API view for activating or deactivating
    a teacher profile.
    """

    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]

    @staticmethod
    def get_service() -> TeacherService:
        """
        Return the teacher service.
        """
        return TeacherService
    @extend_schema(
        request=TeacherStatusSerializer,
        responses=TeacherSerializer,
    )
    def patch(
        self,
        request,
        teacher_id: int,
    ):
        """
        Update the teacher active status
        within the current tenant.
        """

        serializer = TeacherStatusSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        service = self.get_service()

        teacher = service.change_teacher_status(
            tenant=request.tenant,
            teacher_id=teacher_id,
            is_active=serializer.validated_data[
                "is_active"
            ],
        )

        response_serializer = TeacherSerializer(
            teacher,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )
class TeacherDeleteAPIView(APIView):
    """
    API view for soft deleting
    a teacher profile.
    """

    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]
    @staticmethod
    def get_service() -> TeacherService:
        """
        Return the teacher service.
        """
        return TeacherService

    def delete(
        self,
        request,
        teacher_id: int,
    ):
        """
        Soft delete a teacher profile
        within the current tenant.
        """

        self.get_service().delete_teacher(
            tenant=request.tenant,
            teacher_id=teacher_id,
        )

        return Response(
            {
                "message": (
                    "Teacher deleted successfully."
                ),
            },
            status=status.HTTP_200_OK,
        )