from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.core.permissions import IsAdminRole
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import OpenApiResponse, extend_schema
from apps.examinations.serializers import (
    ExaminationCreateSerializer,
    ExaminationSerializer,
    ExaminationStatusSerializer,
    ExaminationUpdateSerializer,
)
from apps.examinations.services import ExaminationService
class ExaminationAPIView(APIView):
    """
    Create, retrieve and update examination.
    """

    def get_permissions(self):
        """
        Assign permissions based on request method.
        """

        if self.request.method == "GET":
            return [ IsAuthenticated(),]

        return [
            IsAuthenticated(),
            IsAdminRole(),
        ]

    @extend_schema(
        request=ExaminationCreateSerializer,
        responses=ExaminationSerializer,
    )
    def post(
        self,
        request,
    ):
        """
        Create an examination for the current tenant.
        """

        serializer = ExaminationCreateSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        examination = (
            ExaminationService.create_examination(
                tenant=request.tenant,
                validated_data=serializer.validated_data,
            )
        )

        response_serializer = ExaminationSerializer(
            examination,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        responses=ExaminationSerializer,
    )
    def get(
        self,
        request,
        examination_id,
    ):
        """
        Retrieve an examination belonging
        to the current tenant.
        """

        examination = (
            ExaminationService.get_examination_by_id(
                tenant=request.tenant,
                examination_id=examination_id,
            )
        )

        serializer = ExaminationSerializer(
            examination,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        request=ExaminationUpdateSerializer,
        responses=ExaminationSerializer,
    )
    def put(
        self,
        request,
        examination_id,
    ):
        """
        Update an examination belonging
        to the current tenant.
        """

        serializer = ExaminationUpdateSerializer(
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        examination = (
            ExaminationService.update_examination(
                tenant=request.tenant,
                examination_id=examination_id,
                validated_data=serializer.validated_data,
            )
        )

        response_serializer = ExaminationSerializer(
            examination,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )


class ExaminationListAPIView(APIView):
    """
    List all examinations for the current tenant.
    """

    permission_classes = []

    @extend_schema(
        responses=ExaminationSerializer,
    )
    def get(
        self,
        request,
    ):
        """
        Retrieve all examinations for
        the current tenant.
        """

        examinations = (
            ExaminationService.list_examinations(
                tenant=request.tenant,
            )
        )

        serializer = ExaminationSerializer(
            examinations,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class ExaminationStatusAPIView(APIView):
    """
    Change examination status.
    """

    permission_classes = [
        IsAdminRole,
    ]

    @extend_schema(
        request=ExaminationStatusSerializer,
        responses=ExaminationSerializer,
    )
    def patch(
        self,
        request,
        examination_id,
    ):
        """
        Change examination status for
        the current tenant.
        """

        serializer = ExaminationStatusSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        examination = (
            ExaminationService.change_examination_status(
                tenant=request.tenant,
                examination_id=examination_id,
                status=serializer.validated_data[
                    "status"
                ],
            )
        )

        response_serializer = ExaminationSerializer(
            examination,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )


class ExaminationDeleteAPIView(APIView):
    """
    Soft delete examination.
    """

    permission_classes = [
        IsAdminRole,
    ]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description=(
                    "Examination deleted successfully."
                ),
            ),
        },
    )
    def delete(
        self,
        request,
        examination_id,
    ):
        """
        Soft delete an examination belonging
        to the current tenant.
        """

        ExaminationService.delete_examination(
            tenant=request.tenant,
            examination_id=examination_id,
        )

        return Response(
            {
                "message": (
                    "Examination deleted successfully."
                ),
            },
            status=status.HTTP_200_OK,
        )