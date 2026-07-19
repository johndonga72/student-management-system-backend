"""
API views for department-related operations.
"""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.core.permissions import IsAdminRole
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
    permission_classes = [IsAuthenticated,IsAdminRole]
    def post(self, request, *args, **kwargs):
        """
        Create a new department.
        """
        serializer = DepartmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        DepartmentService.create_department(
            serializer.validated_data
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

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retrieve all departments.
        """
        departments = DepartmentService.list_departments()

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

    permission_classes = [IsAuthenticated]

    def get(self, request, department_id, *args, **kwargs):
        """
        Retrieve a department by its ID.
        """
        department = DepartmentService.get_department_by_id(
            department_id
        )

        serializer = DepartmentSerializer(department)

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

    def patch(self, request, department_id, *args, **kwargs):
        """
        Update department information.
        """
        department = DepartmentService.get_department_by_id(
            department_id
        )

        serializer = DepartmentUpdateSerializer(
            department,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        DepartmentService.update_department(
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

    def patch(self, request, department_id, *args, **kwargs):
        """
        Change department status.
        """
        serializer = DepartmentStatusSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        DepartmentService.change_department_status(
            department_id=department_id,
            is_active=serializer.validated_data["is_active"],
        )
        return Response(
            {
                "message": "Department status updated successfully."
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
    def delete(self, request, department_id, *args, **kwargs):
        """
        Soft delete a department.
        """
        DepartmentService.delete_department(
            department_id=department_id
        )
        return Response(
            {
                "message": "Department deleted successfully."
            },
            status=status.HTTP_200_OK,
        )
