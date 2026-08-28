"""
Dashboard API views.
"""
from __future__ import annotations
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from apps.core.permissions import IsAdminRole
from apps.dashboard.serializers import DashboardSerializer
from apps.dashboard.services import DashboardService
class DashboardAPIView(APIView):
    """
    API view for the Admin Dashboard.
    """
    permission_classes = [
        IsAdminRole,
    ]
    @extend_schema(
        responses={
            200: DashboardSerializer,
        },
        description=(
            "Retrieve dashboard statistics "
            "for the current tenant."
        ),
    )
    def get(
        self,
        request: Request,
    ) -> Response:
        """
        Retrieve dashboard statistics
        for the current tenant.
        """
        dashboard_data = DashboardService.get_dashboard(
            user=request.user,
            tenant=request.tenant,
        )
        serializer = DashboardSerializer(
            dashboard_data,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )