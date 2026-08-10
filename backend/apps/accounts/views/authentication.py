"""
API views responsible for user authentication.
This module contains endpoints for user registration
and authentication.
"""
from __future__ import annotations
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.accounts.serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    LoginSerializer,
    TokenResponseSerializer
)
from apps.accounts.services import (
    AuthenticationService,
    RegistrationService,
)
from drf_spectacular.utils import extend_schema

class RegisterAPIView(APIView):
    """
    API endpoint for registering a new student account.
    """
    @extend_schema(
        request=UserRegistrationSerializer,
        responses=UserSerializer,
    )
    def post(self, request, *args, **kwargs):
        """
        Register a new student account.
        """
        serializer = UserRegistrationSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        user = RegistrationService.register_user(
            serializer.validated_data,
        )
        response_serializer = UserSerializer(user)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )
class LoginAPIView(APIView):
    """
    API endpoint for user authentication.
    """
    @extend_schema(
        request=LoginSerializer,
        responses=TokenResponseSerializer,
    )
    def post(self, request, *args, **kwargs):
        """
        Authenticate a user and return JWT tokens.

        Args:
            request: Incoming HTTP request.

        Returns:
            Response: JWT tokens and authenticated user details.
        """

        serializer = LoginSerializer(
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        user = AuthenticationService.authenticate_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        response_data = AuthenticationService.generate_tokens(
            user,
        )

        response_serializer = TokenResponseSerializer(
            response_data,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )