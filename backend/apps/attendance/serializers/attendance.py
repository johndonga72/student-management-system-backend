"""
Attendance serializers.
This module contains serializers used for
creating and updating attendance records.
"""
from rest_framework import serializers

from apps.attendance.models import Attendance

from .base import BaseAttendanceSerializer


class AttendanceCreateSerializer(BaseAttendanceSerializer):
    """
    Serializer for creating attendance records.
    """

    class Meta(BaseAttendanceSerializer.Meta):
        model = Attendance

        fields = (
            "student",
            "teacher",
            "subject",
            "attendance_date",
            "status",
            "remarks",
        )
class AttendanceUpdateSerializer(BaseAttendanceSerializer):
    """
    Serializer for updating attendance records.
    """
    class Meta(BaseAttendanceSerializer.Meta):
        model = Attendance
        fields = (
            "status",
            "remarks",
        )