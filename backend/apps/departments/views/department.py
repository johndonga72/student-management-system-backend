"""
API views for department-related operations.
"""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.core.permissions import IsAdminRole
from apps.departments.models import Department
from drf_spectacular.utils import extend_schema
from apps.departments.serializers import (
    DepartmentCreateSerializer,
    DepartmentSerializer,
    DepartmentUpdateSerializer,
    DepartmentStatusSerializer,
)
from apps.departments.services import DepartmentService

class DepartmentCreateAPIView(APIView):
    """
    API view for creating a new department.
    """

    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]
    @extend_schema(
        request=DepartmentCreateSerializer,
        responses={
            201: None,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Create a new department.
        """

        serializer = DepartmentCreateSerializer(
            data=request.data,
            context={
                "tenant": request.tenant,
            },
        )

        serializer.is_valid(
            raise_exception=True,
        )

        DepartmentService.create_department(
            tenant=request.tenant,
            validated_data=serializer.validated_data,
        )

        return Response(
            {
                "message": "Department created successfully."
            },
            status=status.HTTP_201_CREATED,
        )


class DepartmentListAPIView(APIView):
    """
    API view for listing all departments.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, *args, **kwargs):
        """
        Retrieve all departments for the current tenant.
        """

        departments = DepartmentService.list_departments(
            tenant=request.tenant,
        )

        serializer = DepartmentSerializer(
            departments,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class DepartmentDetailAPIView(APIView):
    """
    API view for retrieving department details.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request,
        department_id,
        *args,
        **kwargs,
    ):
        """
        Retrieve a department by its ID
        within the current tenant.
        """

        try:
            department = DepartmentService.get_department_by_id(
                tenant=request.tenant,
                department_id=department_id,
            )
        except Department.DoesNotExist:
            return Response(
                {
                    "message": "Department not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        

        serializer = DepartmentSerializer(
            department,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
class DepartmentUpdateAPIView(APIView):
    """
    API view for updating a department.
    """

    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]
    @extend_schema(
        request=DepartmentUpdateSerializer,
        responses={
            200: None,
        },
    )
    def patch(
        self,
        request,
        department_id,
        *args,
        **kwargs,
    ):
        """
        Update department information.
        """

        department = DepartmentService.get_department_by_id(
            tenant=request.tenant,
            department_id=department_id,
        )

        serializer = DepartmentUpdateSerializer(
            department,
            data=request.data,
            partial=True,
            context={
                "tenant": request.tenant,
            },
        )

        serializer.is_valid(
            raise_exception=True,
        )

        DepartmentService.update_department(
            tenant=request.tenant,
            department_id=department_id,
            validated_data=serializer.validated_data,
        )

        return Response(
            {
                "message": "Department updated successfully."
            },
            status=status.HTTP_200_OK,
        )


class DepartmentStatusAPIView(APIView):
    """
    API view for activating or deactivating a department.
    """

    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]
    @extend_schema(
        request=DepartmentStatusSerializer,
        responses={
            200: None,
        },
    )

    def patch(
        self,
        request,
        department_id,
        *args,
        **kwargs,
    ):
        """
        Change department status.
        """

        serializer = DepartmentStatusSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        DepartmentService.change_department_status(
            tenant=request.tenant,
            department_id=department_id,
            is_active=serializer.validated_data[
                "is_active"
            ],
        )

        return Response(
            {
                "message": (
                    "Department status updated successfully."
                )
            },
            status=status.HTTP_200_OK,
        )


class DepartmentDeleteAPIView(APIView):
    """
    API view for soft deleting a department.
    """

    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]

    def delete(
        self,
        request,
        department_id,
        *args,
        **kwargs,
    ):
        """
        Soft delete a department.
        """

        DepartmentService.delete_department(
            tenant=request.tenant,
            department_id=department_id,
        )

        return Response(
            {
                "message": (
                    "Department deleted successfully."
                )
            },
            status=status.HTTP_200_OK,
        )