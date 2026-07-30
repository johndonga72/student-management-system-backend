"""
Dashboard response serializer.
"""
from rest_framework import serializers
from .base import (
    AcademicSummarySerializer,
    AttendanceSummarySerializer,
    RecentActivitySerializer,
)
class DashboardSerializer(serializers.Serializer):
    """
    Complete Admin Dashboard response.
    """
    academic_summary = AcademicSummarySerializer()
    attendance_summary = AttendanceSummarySerializer()
    recent_activity = RecentActivitySerializer()