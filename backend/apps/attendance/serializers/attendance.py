"""
Attendance serializers.
This module contains serializers used for
creating and updating attendance records.
"""
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
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
            "status",
            "attendance_date",
            "remarks",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Attendance.objects.all(),
                fields=(
                    "student",
                    "subject",
                    "attendance_date",
                ),
                message=(
                    "Attendance has already been marked "
                    "for this student on this date "
                    "for the selected subject."
                ),
            )
        ]
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