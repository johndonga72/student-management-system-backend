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
    CourseUpdateSerializer,
    CourseStatusSerializer,
)
from apps.courses.services import CourseService
from drf_spectacular.utils import OpenApiResponse, extend_schema

class CourseListCreateAPIView(APIView):
    """
    API view for listing and creating courses.
    """
    def get_permissions(self):
        """
        Assign permissions based on request method.
        """
        if self.request.method == "POST":
            return [
                IsAuthenticated(),
                IsAdminRole(),
            ]

        return [
            IsAuthenticated(),
        ]
    @extend_schema(
        responses=CourseSerializer,
    )
    def get(
        self,
        request,
        *args,
        **kwargs,
    ):
        """
        List all courses for the current tenant.
        """

        courses = CourseService.list_courses(
            tenant=request.tenant,
        )

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
    @extend_schema(
        request=CourseCreateSerializer,
        responses=CourseSerializer,
    )
    def post(
        self,
        request,
        *args,
        **kwargs,
    ):
        """
        Create a new course for the current tenant.
        """

        serializer = CourseCreateSerializer(
            data=request.data,
            context={
                "tenant": request.tenant,
            },
        )

        serializer.is_valid(
            raise_exception=True,
        )

        course = CourseService.create_course(
            tenant=request.tenant,
            validated_data=serializer.validated_data,
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

        if self.request.method in [
            "PATCH",
            "DELETE",
        ]:
            return [
                IsAuthenticated(),
                IsAdminRole(),
            ]

        return [
            IsAuthenticated(),
        ]
    @extend_schema(
        responses=CourseSerializer,
    )
    def get(
        self,
        request,
        course_id,
        *args,
        **kwargs,
    ):
        """
        Retrieve course details for the current tenant.
        """

        course = CourseService.get_course_by_id(
            tenant=request.tenant,
            course_id=course_id,
        )

        serializer = CourseSerializer(
            course,
        )

        return Response(
            {
                "message": "Course retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        request=CourseUpdateSerializer,
        responses=CourseSerializer,
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
            context={
                "tenant": request.tenant,
            },
        )

        serializer.is_valid(
            raise_exception=True,
        )

        course = CourseService.update_course(
            tenant=request.tenant,
            course_id=course_id,
            validated_data=serializer.validated_data,
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
    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Course deleted successfully.",
            ),
        },
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
            tenant=request.tenant,
            course_id=course_id,
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
    @extend_schema(
        request=CourseStatusSerializer,
        responses=CourseSerializer,
    )
    def patch(
        self,
        request,
        course_id,
        *args,
        **kwargs,
    ):
        """
        Change course status within the current tenant.
        """

        serializer = CourseStatusSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        course = CourseService.change_course_status(
            tenant=request.tenant,
            course_id=course_id,
            is_active=serializer.validated_data[
                "is_active"
            ],
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