"""
Admin configuration for the courses application.
"""
from django.contrib import admin
from apps.courses.models import Course
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Course model.
    """
    list_display = (
        "id",
        "name",
        "code",
        "department",
        "credits",
        "is_active",
        "created_at",
    )
    list_filter = (
        "department",
        "is_active",
        "is_deleted",
    )
    search_fields = (
        "name",
        "code",
        "department__name",
    )
    ordering = (
        "department",
        "name",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            "Course Information",
            {
                "fields": (
                    "department",
                    "name",
                    "code",
                    "description",
                    "credits",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "is_active",
                    "is_deleted",
                )
            },
        ),
        (
            "Audit Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )