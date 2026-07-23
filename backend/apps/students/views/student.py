"""
Student API views.
"""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.core.permissions import IsAdminRole
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

    def patch(
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
            partial=True,
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
class StudentApprovalAPIView(APIView):
    """
    Handle student approval operations.

    This API allows administrators to approve
    pending student profiles by assigning their
    academic information.
    """

    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]

    def patch(
        self,
        request,
        student_id: int,
    ) -> Response:
        """
        Approve a pending student profile.

        Args:
            request:
                HTTP request object.

            student_id:
                Student primary key.

        Returns:
            Response:
                Approved student details.
        """

        serializer = StudentApprovalSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        student = StudentService.approve_student(
            student_id=student_id,
            validated_data=serializer.validated_data,
        )

        response_serializer = StudentSerializer(
            student,
        )

        return Response(
            {
                "message": (
                    "Student approved successfully."
                ),
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
class StudentStatusAPIView(APIView):
    """
    Handle student status management operations.

    This API allows administrators to update
    the status of a student profile.
    """
    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]
    def patch(
        self,
        request,
        student_id: int,
    ) -> Response:
        """
        Update the status of a student profile.

        Args:
            request:
                HTTP request object.

            student_id:
                Student primary key.

        Returns:
            Response:
                Updated student profile.
        """
        serializer = StudentStatusSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )
        student = StudentService.change_student_status(
            student_id=student_id,
            status=serializer.validated_data["status"],
        )
        response_serializer = StudentSerializer(
            student,
        )
        return Response(
            {
                "message": (
                    "Student status updated successfully."
                ),
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
class StudentDeleteAPIView(APIView):
    """
    Handle student deletion operations.

    This API allows administrators to
    soft delete a student profile.
    """

    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]

    def delete(
        self,
        request,
        student_id: int,
    ) -> Response:
        """
        Soft delete a student profile.

        Args:
            request:
                HTTP request object.

            student_id:
                Student primary key.

        Returns:
            Response:
                Success response.
        """

        StudentService.delete_student(
            student_id=student_id,
        )

        return Response(
            {
                "message": (
                    "Student deleted successfully."
                ),
            },
            status=status.HTTP_200_OK,
        )
