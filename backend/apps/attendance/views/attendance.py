"""
Attendance API views.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.core.permissions import IsAdminRole
from apps.attendance.serializers import (
    AttendanceCreateSerializer,
    AttendanceUpdateSerializer,
    BaseAttendanceSerializer,
)
from apps.attendance.services import AttendanceService
class AttendanceAPIView(APIView):
    """
    API view for attendance operations.
    """
    permission_classes = [IsAdminRole]
    def post(self, request):
        """
        Create a new attendance record.
        """
        serializer = AttendanceCreateSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        attendance = AttendanceService.create_attendance(
            serializer.validated_data
        )

        response_serializer = BaseAttendanceSerializer(
            attendance
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def get(self, request, attendance_id):
        """
        Retrieve attendance details.
        """

        attendance = AttendanceService.get_attendance_by_id(
            attendance_id
        )

        serializer = BaseAttendanceSerializer(
            attendance
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def put(self, request, attendance_id):
        """
        Update attendance record.
        """

        serializer = AttendanceUpdateSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        attendance = AttendanceService.update_attendance(
            attendance_id=attendance_id,
            validated_data=serializer.validated_data,
        )

        response_serializer = BaseAttendanceSerializer(
            attendance
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )


class AttendanceListAPIView(APIView):
    """
    API view for listing attendance records.
    """

    permission_classes = [IsAdminRole]

    def get(self, request):
        """
        Retrieve all attendance records.
        """

        attendance_records = AttendanceService.list_attendance()

        serializer = BaseAttendanceSerializer(
            attendance_records,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )