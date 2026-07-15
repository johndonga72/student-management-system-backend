"""
API views responsible for user profile operations.
"""
from __future__ import annotations
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.accounts.serializers import UserSerializer
class ProfileAPIView(APIView):
    """
    API endpoint for retrieving the authenticated user's profile.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        """
        Return the authenticated user's profile.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)