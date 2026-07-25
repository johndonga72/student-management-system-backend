"""
URL configuration for the subject module.
"""

from django.urls import path

from apps.subjects.views import (
    SubjectAPIView,
    SubjectDeleteAPIView,
    SubjectListAPIView,
    SubjectStatusAPIView,
)

urlpatterns = [
    path(
        "",
        SubjectAPIView.as_view(),
        name="subject-create",
    ),
    path(
        "list/",
        SubjectListAPIView.as_view(),
        name="subject-list",
    ),
    path(
        "<int:subject_id>/",
        SubjectAPIView.as_view(),
        name="subject-detail",
    ),
    path(
        "<int:subject_id>/status/",
        SubjectStatusAPIView.as_view(),
        name="subject-status",
    ),
    path(
        "<int:subject_id>/delete/",
        SubjectDeleteAPIView.as_view(),
        name="subject-delete",
    ),
]