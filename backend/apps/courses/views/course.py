"""
API views for course-related operations.
"""
from __future__ import annotations
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.core.permissions import IsAdminRole
from apps.courses.serializers import (
    CourseCreateSerializer,
    CourseSerializer,
    CourseStatusSerializer,
    CourseUpdateSerializer,
)
from apps.courses.services import CourseService
class CourseListCreateAPIView(APIView):
    """
    API view for listing and creating courses.
    """

    def get_permissions(self):
        """
        Assign permissions based on request method.
        """

        if self.request.method == "POST":
            return [IsAuthenticated(), IsAdminRole()]

        return [IsAuthenticated()]

    def get(self, request, *args, **kwargs):
        """
        List all courses.
        """

        courses = CourseService.list_courses()

        serializer = CourseSerializer(
            courses,
            many=True,
        )

        return Response(
            {
                "message": "Courses retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        """
        Create a new course.
        """

        serializer = CourseCreateSerializer(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        course = CourseService.create_course(
            serializer.validated_data,
        )

        response_serializer = CourseSerializer(
            course,
        )

        return Response(
            {
                "message": "Course created successfully.",
                "data": response_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
class CourseRetrieveUpdateDestroyAPIView(APIView):
    """
    API view for retrieving, updating,
    and deleting a course.
    """
    def get_permissions(self):
        """
        Assign permissions based on request method.
        """
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAuthenticated(), IsAdminRole()]
        return [IsAuthenticated()]
    def get(
        self,
        request,
        course_id,
        *args,
        **kwargs,
    ):
        """
        Retrieve course details.
        """
        course = CourseService.get_course_by_id(
            course_id,
        )
        serializer = CourseSerializer(course)
        return Response(
            {
                "message": "Course retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def patch(
        self,
        request,
        course_id,
        *args,
        **kwargs,
    ):
        """
        Update course information.
        """

        serializer = CourseUpdateSerializer(
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        course = CourseService.update_course(
            course_id,
            serializer.validated_data,
        )

        response_serializer = CourseSerializer(
            course,
        )

        return Response(
            {
                "message": "Course updated successfully.",
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(
        self,
        request,
        course_id,
        *args,
        **kwargs,
    ):
        """
        Soft delete a course.
        """

        CourseService.delete_course(
            course_id,
        )

        return Response(
            {
                "message": "Course deleted successfully.",
            },
            status=status.HTTP_200_OK,
        )
class CourseStatusAPIView(APIView):
    """
    API view for activating or
    deactivating a course.
    """
    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]
    def patch(
        self,
        request,
        course_id,
        *args,
        **kwargs,
    ):
        """
        Change course status.
        """
        serializer = CourseStatusSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )
        course = CourseService.change_course_status(
            course_id,
            serializer.validated_data["is_active"],
        )
        response_serializer = CourseSerializer(
            course,
        )
        return Response(
            {
                "message": "Course status updated successfully.",
                "data": response_serializer.data,
            },
            status=status.HTTP_200_OK,
        )