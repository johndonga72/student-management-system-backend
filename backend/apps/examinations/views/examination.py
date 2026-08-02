from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.permissions import IsAdminRole

from apps.examinations.serializers import (
    ExaminationCreateSerializer,
    ExaminationSerializer,
    ExaminationStatusSerializer,
    ExaminationUpdateSerializer,
)
from apps.examinations.services import ExaminationService
class ExaminationAPIView(APIView):
    """
    Create, Retrieve and Update Examination.
    """

    def get_permissions(self):
        """
        Assign permissions based on request method.
        """
        if self.request.method == "GET":
            return []

        return [IsAdminRole()]

    def post(self, request):
        serializer = ExaminationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        examination = ExaminationService.create_examination(
            serializer.validated_data
        )

        response_serializer = ExaminationSerializer(examination)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def get(self, request, examination_id):
        examination = ExaminationService.get_examination_by_id(
            examination_id
        )

        serializer = ExaminationSerializer(examination)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, examination_id):
        serializer = ExaminationUpdateSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        examination = ExaminationService.update_examination(
            examination_id,
            serializer.validated_data,
        )

        response_serializer = ExaminationSerializer(
            examination
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )
        
class ExaminationListAPIView(APIView):
    """
    List all examinations.
    """

    permission_classes = []

    def get(self, request):
        examinations = ExaminationService.list_examinations()

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

    permission_classes = [IsAdminRole]

    def patch(self, request, examination_id):
        serializer = ExaminationStatusSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        examination = ExaminationService.change_examination_status(
            examination_id,
            serializer.validated_data["status"],
        )

        response_serializer = ExaminationSerializer(
            examination
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )
class ExaminationDeleteAPIView(APIView):
    """
    Soft delete examination.
    """

    permission_classes = [IsAdminRole]

    def delete(self, request, examination_id):
        ExaminationService.delete_examination(
            examination_id
        )

        return Response(
            {
                "message": "Examination deleted successfully."
            },
            status=status.HTTP_200_OK,
        )