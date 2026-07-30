"""
Dashboard serializer exports.
"""
from .base import (
    AcademicSummarySerializer,
    AttendanceSummarySerializer,
    RecentActivitySerializer,
)
from .dashboard import DashboardSerializer
__all__ = [
    "AcademicSummarySerializer",
    "AttendanceSummarySerializer",
    "RecentActivitySerializer",
    "DashboardSerializer",
]