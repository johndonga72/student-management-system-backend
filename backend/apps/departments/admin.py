"""
Admin configuration for the departments application.
"""
from django.contrib import admin
from apps.departments.models import Department
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Department model.
    """
    list_display = (
        "id",
        "code",
        "name",
        "is_active",
        "created_at",
    )
    list_filter = (
        "is_active",
        "created_at",
    )
    search_fields = (
        "name",
        "code",
    )
    ordering = ("name",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )