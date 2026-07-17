"""
URL configuration for the departments application.
"""

from django.urls import path

from apps.departments.views import DepartmentCreateAPIView

app_name = "departments"

urlpatterns = [
    path(
        "",
        DepartmentCreateAPIView.as_view(),
        name="create",
    ),
]