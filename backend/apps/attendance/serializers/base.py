"""
Attendance base serializer.

This module defines the base serializer used
for attendance responses.

"""
from rest_framework import serializers

from apps.attendance.models import Attendance

class BaseAttendanceSerializer(serializers.ModelSerializer):
    
    """
    Base serializer for attendance records.
    """

    student_number = serializers.CharField(
        source="student.student_number",
        read_only=True,
    )

    student_email = serializers.EmailField(
        source="student.user.email",
        read_only=True,
    )

    teacher_employee_id = serializers.CharField(
        source="teacher.employee_id",
        read_only=True,
    )

    teacher_email = serializers.EmailField(
        source="teacher.user.email",
        read_only=True,
    )

    subject_name = serializers.CharField(
        source="subject.subject_name",
        read_only=True,
    )

    subject_code = serializers.CharField(
        source="subject.subject_code",
        read_only=True,
    )

    course_name = serializers.CharField(
        source="subject.course.name",
        read_only=True,
    )

    department_name = serializers.CharField(
        source="subject.course.department.name",
        read_only=True,
    )

    class Meta:
        model = Attendance

        fields = (
            "id",
            "student",
            "student_number",
            "student_email",
            "teacher",
            "teacher_employee_id",
            "teacher_email",
            "subject",
            "subject_name",
            "subject_code",
            "course_name",
            "department_name",
            "attendance_date",
            "status",
            "remarks",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )