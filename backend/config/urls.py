"""
Root URL configuration for the Student Management System.
"""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.accounts.urls")),
    path("api/v1/departments/",include("apps.departments.urls")),
    path("api/v1/courses/",include("apps.courses.urls")),
    path("api/v1/students/",include("apps.students.urls")),
    path("api/v1/subjects/",include("apps.subjects.urls")),
    path("api/v1/teachers/",include("apps.teachers.urls")),
    path("api/v1/attendance/",include("apps.attendance.urls")),
    path("api/v1/examinations/",include("apps.examinations.urls")),
    path("api/v1/results/",include("apps.results.urls")),
    path("api/v1/dashboard/",include("apps.dashboard.urls")),
    path("api/v1/tenants/",include("apps.tenants.urls")),
    path("api/v1/schema/",SpectacularAPIView.as_view(),name="schema",),
    path("api/v1/docs/",SpectacularSwaggerView.as_view(url_name="schema",), name="swagger-ui",
    ),
]
