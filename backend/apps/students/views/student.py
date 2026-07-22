"""
Student API views.
"""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from core.permissions import IsAdminRole
from apps.students.serializers import (
    StudentApprovalSerializer,
    StudentCreateSerializer,
    StudentSerializer,
    StudentStatusSerializer,
    StudentUpdateSerializer,
)
from apps.students.services import StudentService
class StudentProfileAPIView(APIView):
    """
    Handle student profile operations.

    Students can create, retrieve and update
    their own profile.
    """
    permission_classes = [
        IsAuthenticated,
    ]
    def post(
        self,
        request,
    ):
        """
        Create a student profile.
        """
        serializer = StudentCreateSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )
        student = StudentService.create_student_profile(
            user=request.user,
            validated_data=serializer.validated_data,
        )
        response_serializer = StudentSerializer(
            student,
        )
        return Response(
            {
                "message": (
                    "Student profile created successfully."
                ),
                "data": response_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )

    def get(
        self,
        request,
    ):
        """
        Retrieve the authenticated student's profile.
        """

        student = StudentService.get_my_profile(
            request.user,
        )

        serializer = StudentSerializer(
            student,
        )

        return Response(
            {
                "message": "Student profile retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(
        self,
        request,
    ):
        """
        Update the authenticated student's profile.
        """

        student = StudentService.get_my_profile(
            request.user,
        )

        serializer = StudentUpdateSerializer(
            student,
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        student = StudentService.update_student_profile(
            student,
            serializer.validated_data,
        )

        response_serializer = StudentSerializer(
            student,
        )

        return Response(
            {
                "message": (
                    "Student profile updated successfully."
                ),
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
class StudentListAPIView(APIView):
    """
    Handle student listing operations.

    This API is intended for administrative users.
    It supports retrieving all students or filtering
    students by status.
    """
    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]
    def get(
        self,
        request,
    ) -> Response:
        """
        Retrieve student profiles.

        Query Parameters:
            status:
                Optional student status filter.

        Returns:
            Response:
                Serialized student data.
        """

        status_filter = request.query_params.get(
            "status"
        )
        if (
            status_filter
            and status_filter.upper() == "PENDING"
        ):
            students = (
                StudentService.list_pending_students()
            )
        else:
            students = (
                StudentService.list_students()
            )
        serializer = StudentSerializer(
            students,
            many=True,
        )
        return Response(
            {
                "message": (
                    "Students retrieved successfully."
                ),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )