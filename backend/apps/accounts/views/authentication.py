"""
API views responsible for user authentication.

This module contains endpoints for user registration
and authentication.
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.serializers import (
    LoginSerializer,
    TokenResponseSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)
from apps.accounts.services import (
    AuthenticationService,
    RegistrationService,
)


class RegisterAPIView(APIView):
    """
    API endpoint for registering a new student account.
    """

    @extend_schema(
        request=UserRegistrationSerializer,
        responses={
            201: UserSerializer,
        },
    )
    def post(
        self,
        request,
        *args,
        **kwargs,
    ):
        """
        Register a new student account
        within the current tenant.
        """

        serializer = UserRegistrationSerializer(
            data=request.data,
            context={
                "tenant": request.tenant,
            },
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = RegistrationService.register_user(
            tenant=request.tenant,
            validated_data=serializer.validated_data,
        )

        response_serializer = UserSerializer(
            user,
        )

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
        responses={
            200: TokenResponseSerializer,
        },
    )
    def post(
        self,
        request,
        *args,
        **kwargs,
    ):
        """
        Authenticate a user within the current tenant
        and return JWT tokens.

        Args:
            request:
                Incoming HTTP request.

        Returns:
            Response:
                JWT tokens and authenticated user details.
        """

        serializer = LoginSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = AuthenticationService.authenticate_user(
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
            tenant=request.tenant,
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
        