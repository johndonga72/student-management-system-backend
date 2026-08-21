"""
Attendance API views.
"""
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.attendance.serializers import (
    AttendanceCreateSerializer,
    AttendanceUpdateSerializer,
    BaseAttendanceSerializer,
)
from apps.attendance.services import AttendanceService
from apps.core.permissions import IsAdminRole
class AttendanceAPIView(APIView):
    """
    API view for attendance operations.
    """
    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]

    @extend_schema(
        request=AttendanceCreateSerializer,
        responses=BaseAttendanceSerializer,
    )
    def post(self, request):
        """
        Create a new attendance record
        within the current tenant.
        """

        serializer = AttendanceCreateSerializer(
            data=request.data,
            context={
                "tenant": request.tenant,
            },
        )

        serializer.is_valid(
            raise_exception=True,
        )

        attendance = AttendanceService.create_attendance(
            tenant=request.tenant,
            validated_data=serializer.validated_data,
        )

        response_serializer = BaseAttendanceSerializer(
            attendance,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        responses=BaseAttendanceSerializer,
    )
    def get(
        self,
        request,
        attendance_id: int,
    ):
        """
        Retrieve attendance details
        within the current tenant.
        """

        attendance = (
            AttendanceService.get_attendance_by_id(
                tenant=request.tenant,
                attendance_id=attendance_id,
            )
        )

        serializer = BaseAttendanceSerializer(
            attendance,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        request=AttendanceUpdateSerializer,
        responses=BaseAttendanceSerializer,
    )
    def put(
        self,
        request,
        attendance_id: int,
    ):
        """
        Update an attendance record
        within the current tenant.
        """

        serializer = AttendanceUpdateSerializer(
            data=request.data,
            partial=True,
            context={
                "tenant": request.tenant,
            },
        )

        serializer.is_valid(
            raise_exception=True,
        )

        attendance = AttendanceService.update_attendance(
            tenant=request.tenant,
            attendance_id=attendance_id,
            validated_data=serializer.validated_data,
        )

        response_serializer = BaseAttendanceSerializer(
            attendance,
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )


class AttendanceListAPIView(APIView):
    """
    API view for listing attendance records.
    """

    permission_classes = [
        IsAuthenticated,
        IsAdminRole,
    ]

    @extend_schema(
        responses=BaseAttendanceSerializer(
            many=True,
        ),
    )
    def get(self, request):
        """
        Retrieve all attendance records
        for the current tenant.
        """

        attendance_records = (
            AttendanceService.list_attendance(
                tenant=request.tenant,
            )
        )
        serializer = BaseAttendanceSerializer(
            attendance_records,
            many=True,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
