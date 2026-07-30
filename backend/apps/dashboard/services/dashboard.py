"""
Dashboard service layer.
"""

from django.db.models import Count
from django.utils import timezone
from apps.accounts.models import UserRole
from apps.attendance.models import Attendance
from apps.attendance.models.choices import AttendanceStatus
from apps.courses.models import Course
from apps.departments.models import Department
from apps.students.models import Student
from apps.subjects.models import Subject
from apps.teachers.models import Teacher

class DashboardService:
    """
    Service class for dashboard business logic.
    """
# private helper function
    @classmethod
    def _get_academic_summary(cls) -> dict:
        """
        Retrieve overall academic summary statistics.
        """
        return {
            "total_students": Student.objects.count(),
            "total_teachers": Teacher.objects.count(),
            "total_departments": Department.objects.count(),
            "total_courses": Course.objects.count(),
            "total_subjects": Subject.objects.count(),
        }
    @classmethod
    def _get_attendance_summary(cls) -> dict:
        """
        Retrieve today's attendance summary statistics.
        """

        today = timezone.localdate()

        attendance_queryset = Attendance.objects.filter(
            attendance_date=today
        )

        total_attendance = attendance_queryset.count()

        present_count = attendance_queryset.filter(
            status=AttendanceStatus.PRESENT
        ).count()

        absent_count = attendance_queryset.filter(
            status=AttendanceStatus.ABSENT
        ).count()

        late_count = attendance_queryset.filter(
            status=AttendanceStatus.LATE
        ).count()

        attendance_percentage = (
            round((present_count / total_attendance) * 100, 2)
            if total_attendance > 0
            else 0.0
        )

        return {
            "total_attendance": total_attendance,
            "present_count": present_count,
            "absent_count": absent_count,
            "late_count": late_count,
            "attendance_percentage": attendance_percentage,
        }
    @classmethod
    def _get_recent_activity(cls) -> dict:
        """
        Retrieve recent activity across the system.
        """

        recent_students = (
            Student.objects
            .select_related("user")
            .order_by("-created_at")[:5]
            .values(
                "student_number",
                "user__email",
                "created_at",
            )
        )

        recent_teachers = (
            Teacher.objects
            .select_related("user")
            .order_by("-created_at")[:5]
            .values(
                "employee_id",
                "user__email",
                "created_at",
            )
        )

        recent_subjects = (
            Subject.objects
            .order_by("-created_at")[:5]
            .values(
                "subject_code",
                "subject_name",
                "created_at",
            )
        )

        return {
            "recent_students": list(recent_students),
            "recent_teachers": list(recent_teachers),
            "recent_subjects": list(recent_subjects),
        }
# public methods
    @classmethod
    def get_admin_dashboard(cls, user) -> dict:
        """
        Retrieve Admin Dashboard statistics.
        """

        academic_summary = cls._get_academic_summary()

        attendance_summary = cls._get_attendance_summary()

        recent_activity = cls._get_recent_activity()

        return {
            "academic_summary": academic_summary,
            "attendance_summary": attendance_summary,
            "recent_activity": recent_activity,
        }
    @classmethod
    def get_dashboard(cls, user) -> dict:
        """
        Retrieve dashboard based on the authenticated user's role.
        """
        if user.role == UserRole.ADMIN:
            return cls.get_admin_dashboard(user)
        raise ValueError("Dashboard is not available for this user role.")