"""
API views for the Tenant module.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.tenants.models import Tenant
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.core.permissions import IsAdminRole
from apps.tenants.serializers import (
    TenantCreateSerializer,
    TenantSerializer,
    TenantUpdateSerializer,
    TenantStatusSerializer,
)
from apps.tenants.services import TenantService
class TenantAPIView(APIView):
    """
    API view for tenant create, retrieve and update operations.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminRole]
    
    def post(self, request):
        """
        Create a new tenant.
        """

        serializer = TenantCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tenant = TenantService.create_tenant(
            validated_data=serializer.validated_data
        )

        response_serializer = TenantSerializer(tenant)

        return Response(
            {
                "message": "Tenant created successfully.",
                "data": response_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
    def get(self, request, tenant_id: int):
        """
        Retrieve tenant details.
        """

        try:
            tenant = TenantService.get_tenant_by_id(
                tenant_id=tenant_id
            )

            serializer = TenantSerializer(tenant)

            return Response(
                {
                    "message": "Tenant retrieved successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Tenant.DoesNotExist:
            return Response(
                {
                    "message": "Tenant not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
    def _update(self, request, tenant_id: int, partial: bool = False):
        """
        Update an existing tenant.
        """

        serializer = TenantUpdateSerializer(
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(raise_exception=True)

        try:
            tenant = TenantService.update_tenant(
                tenant_id=tenant_id,
                validated_data=serializer.validated_data,
            )

            response_serializer = TenantSerializer(tenant)

            return Response(
                {
                    "message": "Tenant updated successfully.",
                    "data": response_serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Tenant.DoesNotExist:
            return Response(
                {
                    "message": "Tenant not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
    def put(self, request, tenant_id: int):
        """
        Fully update an existing tenant.
        """

        return self._update(
            request=request,
            tenant_id=tenant_id,
            partial=False,
        )
    def patch(self, request, tenant_id: int):
        """
        Partially update an existing tenant.
        """

        return self._update(
            request=request,
            tenant_id=tenant_id,
            partial=True,
        )
class TenantListAPIView(APIView):
    """
    API view for listing all active tenants.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):
        """
        Retrieve all active tenants.
        """

        tenants = TenantService.list_tenants()

        serializer = TenantSerializer(
            tenants,
            many=True,
        )

        return Response(
            {
                "message": "Tenants retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
class TenantStatusAPIView(APIView):
    """
    API view for changing tenant status.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminRole]

    def patch(self, request, tenant_id: int):
        """
        Change tenant status.
        """

        serializer = TenantStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            tenant = TenantService.change_tenant_status(
                tenant_id=tenant_id,
                status=serializer.validated_data["status"],
            )

            response_serializer = TenantSerializer(tenant)

            return Response(
                {
                    "message": "Tenant status updated successfully.",
                    "data": response_serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Tenant.DoesNotExist:
            return Response(
                {
                    "message": "Tenant not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
class TenantDeleteAPIView(APIView):
    """
    API view for soft deleting a tenant.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminRole]

    def delete(self, request, tenant_id: int):
        """
        Soft delete a tenant.
        """

        try:
            TenantService.delete_tenant(
                tenant_id=tenant_id,
            )

            return Response(
                {
                    "message": "Tenant deleted successfully."
                },
                status=status.HTTP_200_OK,
            )

        except Tenant.DoesNotExist:
            return Response(
                {
                    "message": "Tenant not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )  