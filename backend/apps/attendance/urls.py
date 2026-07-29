"""
Attendance URL configuration.
"""
from django.urls import path
from apps.attendance.views import (
    AttendanceAPIView,
    AttendanceListAPIView,
)
app_name = "attendance"
urlpatterns = [
    path(
        "",
        AttendanceAPIView.as_view(),
        name="attendance",
    ),
    path(
        "<int:attendance_id>/",
        AttendanceAPIView.as_view(),
        name="attendance-detail",
    ),
    path(
        "list/",
        AttendanceListAPIView.as_view(),
        name="attendance-list",
    ),
]