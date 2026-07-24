"""
Admin configuration for the Subject model.
"""

from django.contrib import admin

from apps.subjects.models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Subject model.
    """

    list_display = (
        "subject_name",
        "subject_code",
        "course",
        "semester",
        "credits",
        "is_active",
        "is_deleted",
        "created_at",
    )

    list_filter = (
        "course",
        "semester",
        "is_active",
        "is_deleted",
    )

    search_fields = (
        "subject_name",
        "subject_code",
        "course__course_name",
    )

    ordering = (
        "semester",
        "subject_name",
    )

    list_select_related = (
        "course",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Subject Information",
            {
                "fields": (
                    "course",
                    "subject_name",
                    "subject_code",
                    "semester",
                    "credits",
                    "description",
                ),
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "is_active",
                    "is_deleted",
                ),
            },
        ),
        (
            "Audit Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )