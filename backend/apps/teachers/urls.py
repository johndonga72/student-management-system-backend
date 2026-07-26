"""
Teacher URL configuration.

This module defines API routes for
teacher management.
"""
from django.urls import path
from apps.teachers.views import (
    TeacherAPIView,
    TeacherDeleteAPIView,
    TeacherListAPIView,
    TeacherStatusAPIView,
)
app_name = "teachers"
urlpatterns = [
    path(
        "",
        TeacherAPIView.as_view(),
        name="teacher-create",
    ),
    path(
        "list/",
        TeacherListAPIView.as_view(),
        name="teacher-list",
    ),
    path(
        "<int:teacher_id>/",
        TeacherAPIView.as_view(),
        name="teacher-detail",
    ),
    path(
        "<int:teacher_id>/status/",
        TeacherStatusAPIView.as_view(),
        name="teacher-status",
    ),
    path(
        "<int:teacher_id>/delete/",
        TeacherDeleteAPIView.as_view(),
        name="teacher-delete",
    ),
]