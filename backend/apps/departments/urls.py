"""
URL configuration for the departments application.
"""

from django.urls import path

from apps.departments.views import DepartmentCreateAPIView,DepartmentListAPIView,DepartmentDetailAPIView,DepartmentUpdateAPIView,DepartmentStatusAPIView,DepartmentDeleteAPIView

app_name = "departments"

urlpatterns = [
    path(
        "",
        DepartmentListAPIView.as_view(),
        name="list",
    ),
    path(
        "create/",
        DepartmentCreateAPIView.as_view(),
        name="create",
    ),
    path(
        "<int:department_id>/",
        DepartmentDetailAPIView.as_view(),
        name="detail",
    ),
        path(
        "<int:department_id>/update/",
        DepartmentUpdateAPIView.as_view(),
        name="update",
    ),
    path(
        "<int:department_id>/status/",
        DepartmentStatusAPIView.as_view(),
        name="status",
    ),
    path(
        "<int:department_id>/delete/",
        DepartmentDeleteAPIView.as_view(),
        name="delete",
    ),
]
