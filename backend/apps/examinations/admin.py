"""
Admin configuration for the Examination module.
"""

from django.contrib import admin

from apps.examinations.models import Examination


@admin.register(Examination)
class ExaminationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Examination.
    """

    list_display = (
        "id",
        "subject",
        "teacher",
        "exam_type",
        "semester",
        "academic_year",
        "exam_date",
        "maximum_marks",
        "passing_marks",
        "status",
    )

    list_filter = (
        "exam_type",
        "semester",
        "academic_year",
        "status",
        "exam_date",
    )

    search_fields = (
        "subject__subject_name",
        "teacher__user__email",
        "academic_year",
    )

    ordering = (
        "-exam_date",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Examination Information",
            {
                "fields": (
                    "subject",
                    "teacher",
                    "exam_type",
                    "semester",
                    "academic_year",
                    "exam_date",
                ),
            },
        ),
        (
            "Marks Configuration",
            {
                "fields": (
                    "maximum_marks",
                    "passing_marks",
                ),
            },
        ),
        (
            "Additional Information",
            {
                "fields": (
                    "instructions",
                    "status",
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