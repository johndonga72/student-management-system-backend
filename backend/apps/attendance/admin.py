"""
Attendance admin configuration.
"""
from django.contrib import admin
from apps.attendance.models import Attendance
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Attendance model.
    """

    list_display = (
        "student",
        "teacher",
        "subject",
        "attendance_date",
        "status",
    )

    list_filter = (
        "status",
        "attendance_date",
        "subject",
        "teacher",
    )

    search_fields = (
        "student__user__first_name",
        "student__user__last_name",
        "student__user__email",
        "teacher__user__first_name",
        "teacher__user__last_name",
        "teacher__employee_id",
        "subject__subject_name",
        "subject__subject_code",
    )

    ordering = (
        "-attendance_date",
        "student",
    )
    
    date_hierarchy = "attendance_date"

    list_select_related = (
        "student",
        "teacher",
        "subject",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    list_per_page = 25