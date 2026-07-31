"""
Dashboard API views.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.core.permissions import IsAdminRole
from apps.dashboard.serializers import DashboardSerializer
from apps.dashboard.services import DashboardService
class DashboardAPIView(APIView):
    """
    API view for the Admin Dashboard.
    """

    permission_classes = [IsAdminRole]

    def get(self, request):
        """
        Retrieve dashboard statistics.
        """

        dashboard_data = DashboardService.get_dashboard(
            request.user
        )

        serializer = DashboardSerializer(
            dashboard_data
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )