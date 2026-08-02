"""
Result API views.
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsAdminRole

from apps.results.serializers import (
    ResultCreateSerializer,
    ResultSerializer,
    ResultUpdateSerializer,
    ResultStatusSerializer
)
from apps.results.services import ResultService


class ResultAPIView(APIView):
    """
    API view for creating, retrieving,
    and updating results.
    """

    def get_permissions(self):
        """
        Return permissions based on request method.
        """

        if self.request.method in ["POST", "PUT"]:
            permission_classes = [
                IsAuthenticated,
                IsAdminRole,
            ]
        else:
            permission_classes = [
                IsAuthenticated,
            ]

        return [
            permission()
            for permission in permission_classes
        ]

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Create a new result.
        """

        serializer = ResultCreateSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        result = ResultService.create_result(
            serializer.validated_data,
        )

        response = ResultSerializer(
            result,
        )

        return Response(
            response.data,
            status=status.HTTP_201_CREATED,
        )

    def get(
        self,
        request: Request,
        result_id: int,
    ) -> Response:
        """
        Retrieve a result by its identifier.
        """

        result = ResultService.get_result_by_id(
            result_id,
        )

        serializer = ResultSerializer(
            result,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def put(
        self,
        request: Request,
        result_id: int,
    ) -> Response:
        """
        Update an existing result.
        """

        serializer = ResultUpdateSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        result = ResultService.update_result(
            result_id=result_id,
            validated_data=serializer.validated_data,
        )

        response = ResultSerializer(
            result,
        )

        return Response(
            response.data,
            status=status.HTTP_200_OK,
        )
class ResultListAPIView(APIView):
    """
    API view for listing results.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request: Request,
    ) -> Response:
        """
        Retrieve all active results.
        """

        results = ResultService.list_results()

        serializer = ResultSerializer(
            results,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
class ResultStatusAPIView(APIView):
    """
    API view for updating the status of a result.
    """

    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]

    def patch(
        self,
        request: Request,
        result_id: int,
    ) -> Response:
        """
        Update the status of a result.
        """

        serializer = ResultStatusSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        result = ResultService.change_result_status(
            result_id=result_id,
            status=serializer.validated_data["status"],
        )

        response = ResultSerializer(
            result,
        )

        return Response(
            response.data,
            status=status.HTTP_200_OK,
        )
class ResultDeleteAPIView(APIView):
    """
    API view for soft deleting a result.
    """
    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]
    def delete(
        self,
        request: Request,
        result_id: int,
    ) -> Response:
        """
        Soft delete a result.
        """
        ResultService.delete_result(
            result_id=result_id,
        )
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )