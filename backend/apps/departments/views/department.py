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