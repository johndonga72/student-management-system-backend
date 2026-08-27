"""
API views responsible for user profile operations.
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from apps.accounts.serializers import UserSerializer


class ProfileAPIView(APIView):
    """
    API endpoint for retrieving the authenticated user's profile.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    @extend_schema(
        responses=UserSerializer,
    )
    def get(
        self,
        request: Request,
        *args,
        **kwargs,
    ) -> Response:
        """
        Return the authenticated user's profile
        within the current tenant.
        """

        user = request.user

        # -------------------------------------------------
        # Tenant isolation check
        # -------------------------------------------------

        if user.tenant_id != request.tenant.id:
            return Response(
                {
                    "message": (
                        "User does not belong to the current tenant."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = UserSerializer(
            user,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )