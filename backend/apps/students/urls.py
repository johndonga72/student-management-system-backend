"""
URL configuration for the student module.

This module defines the API endpoints for student
profile management and administrative operations.
"""
from django.urls import path
from apps.students.views import (
    StudentApprovalAPIView,
    StudentDeleteAPIView,
    StudentListAPIView,
    StudentProfileAPIView,
    StudentStatusAPIView,
)
app_name = "students"
urlpatterns = [
    path(
        "profile/",
        StudentProfileAPIView.as_view(),
        name="student-profile",
    ),
    path(
        "",
        StudentListAPIView.as_view(),
        name="student-list",
    ),
    path(
        "<int:student_id>/approve/",
        StudentApprovalAPIView.as_view(),
        name="student-approve",
    ),
    path(
        "<int:student_id>/status/",
        StudentStatusAPIView.as_view(),
        name="student-status",
    ),
    path(
        "<int:student_id>/",
        StudentDeleteAPIView.as_view(),
        name="student-delete",
    ),
]