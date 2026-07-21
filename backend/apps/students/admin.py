"""
Admin configuration for the Student module.
"""
from django.contrib import admin
from apps.students.models import Student
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Student model.
    """
    list_display = (
        "student_number",
        "user",
        "department",
        "course",
        "semester",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "department",
        "course",
        "semester",
        "gender",
        "is_deleted",
    )
    search_fields = (
        "student_number",
        "user__first_name",
        "user__last_name",
        "user__email",
        "phone",
    )
    readonly_fields = (
        "student_number",
        "created_at",
        "updated_at",
    )
    ordering = (
        "student_number",
    )
    list_per_page = 20
    fieldsets = (
        (
            "Account Information",
            {
                "fields": (
                    "user",
                    "student_number",
                    "status",
                )
            },
        ),
        (
            "Academic Information",
            {
                "fields": (
                    "department",
                    "course",
                    "semester",
                    "section",
                    "admission_date",
                )
            },
        ),
        (
            "Personal Information",
            {
                "fields": (
                    "date_of_birth",
                    "gender",
                    "phone",
                    "address",
                    "guardian_name",
                    "guardian_phone",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "is_deleted",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )