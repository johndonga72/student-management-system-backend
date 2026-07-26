"""
Teacher API views.

This module contains API views for managing
teacher operations.
"""
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
    def post(self, request):
        """
        Create a teacher profile.
        """
        serializer = TeacherCreateSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )
        service = self.get_service()

        teacher = service.create_teacher(
            serializer.validated_data,
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
        Retrieve teacher information.
        """
        service = self.get_service()

        if teacher_id is None:

            teachers = service.list_teachers()

            serializer = TeacherSerializer(
                teachers,
                many=True,
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        teacher = service.get_teacher_by_id(
            teacher_id,
        )

        serializer = TeacherSerializer(
            teacher,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    def put(
        self,
        request,
        teacher_id: int,
    ):
        """
        Update a teacher profile.
        """
        serializer = TeacherUpdateSerializer(
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        teacher = self.get_service().update_teacher(
            teacher_id,
            serializer.validated_data,
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

    def get(self, request):
        """
        Retrieve all teacher profiles.
        """
        service = self.get_service()

        teachers = service.list_teachers()

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

    def patch(
        self,
        request,
        teacher_id: int,
    ):
        """
        Update the teacher active status.
        """
        serializer = TeacherStatusSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )
        service = self.get_service()
        teacher = service.change_teacher_status(
            teacher_id=teacher_id,
            is_active=serializer.validated_data["is_active"],
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
        Soft delete a teacher profile.
        """
        self.get_service().delete_teacher(
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