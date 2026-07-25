"""
Root URL configuration for the Student Management System.
"""
from django.contrib import admin
from django.urls import include, path
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.accounts.urls")),
    path("api/v1/departments/",include("apps.departments.urls")),
    path("api/v1/courses/",include("apps.courses.urls")),
    path("api/v1/students/",include("apps.students.urls")),
    path("api/v1/subjects/",include("apps.subjects.urls")),
]
