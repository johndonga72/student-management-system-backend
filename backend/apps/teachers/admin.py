"""
Teacher admin configuration.
This module configures the Django admin interface
for the Teacher model.
"""
from django.contrib import admin
from apps.teachers.models import Teacher
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Teacher model.
    """
    list_display = (
        "employee_id",
        "user",
        "department",
        "designation",
        "experience_years",
        "joining_date",
        "is_active",
    )
    list_filter = (
        "department",
        "designation",
        "is_active",
        "is_deleted",
    )
    list_select_related = (
    "user",
    "department",
    )
    list_per_page = 25
    date_hierarchy = "joining_date"
    
    search_fields = (
        "employee_id",
        "user__first_name",
        "user__last_name",
        "user__email",
        "department__department_name",
    )
    ordering = (
        "employee_id",
    )
    filter_horizontal = (
        "subjects",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            "User Information",
            {
                "fields": (
                    "user",
                    "employee_id",
                ),
            },
        ),
        (
            "Professional Information",
            {
                "fields": (
                    "department",
                    "designation",
                    "qualification",
                    "specialization",
                    "experience_years",
                    "joining_date",
                    "subjects",
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
