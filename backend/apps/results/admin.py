from django.contrib import admin
from apps.results.models import Result
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    """
    Admin configuration for Result model.
    """
    list_display = (
        "id",
        "student",
        "examination",
        "obtained_marks",
        "result_status",
        "status",
        "created_at",
    )
    list_filter = (
        "result_status",
        "status",
        "is_deleted",
        "created_at",
    )
    search_fields = (
        "student__user__full_name",
        "student__user__email",
        "examination__subject__subject_name",
    )
    ordering = (
        "-created_at",
    )
    list_per_page = 20
    readonly_fields = (
        "created_at",
        "updated_at",
    )