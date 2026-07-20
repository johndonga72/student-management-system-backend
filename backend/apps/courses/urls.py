"""
URL configuration for course-related APIs.
"""
from django.urls import path
from apps.courses.views import (
    CourseListCreateAPIView,
    CourseRetrieveUpdateDestroyAPIView,
    CourseStatusAPIView,
)
app_name = "courses"
urlpatterns = [
    path(
        "",
        CourseListCreateAPIView.as_view(),
        name="course-list-create",
    ),
    path(
        "<int:course_id>/",
        CourseRetrieveUpdateDestroyAPIView.as_view(),
        name="course-detail",
    ),
    path(
        "<int:course_id>/status/",
        CourseStatusAPIView.as_view(),
        name="course-status",
    ),
]