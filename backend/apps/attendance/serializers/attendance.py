from rest_framework import serializers

from apps.attendance.models import Attendance
from apps.students.models import Student
from apps.subjects.models import Subject
from apps.teachers.models import Teacher

from .base import BaseAttendanceSerializer


class AttendanceCreateSerializer(
    BaseAttendanceSerializer
):
    """
    Serializer for creating attendance records.
    """

    class Meta(BaseAttendanceSerializer.Meta):
        model = Attendance

        fields = (
            "student",
            "teacher",
            "subject",
            "status",
            "attendance_date",
            "remarks",
        )

    def validate(self, attrs):
        """
        Validate that all related objects belong
        to the current tenant.
        """

        tenant = self.context["tenant"]

        student = attrs["student"]
        teacher = attrs["teacher"]
        subject = attrs["subject"]

        if student.tenant_id != tenant.id:
            raise serializers.ValidationError(
                {
                    "student": (
                        "Selected student does not "
                        "belong to the current tenant."
                    )
                }
            )

        if teacher.tenant_id != tenant.id:
            raise serializers.ValidationError(
                {
                    "teacher": (
                        "Selected teacher does not "
                        "belong to the current tenant."
                    )
                }
            )

        if subject.tenant_id != tenant.id:
            raise serializers.ValidationError(
                {
                    "subject": (
                        "Selected subject does not "
                        "belong to the current tenant."
                    )
                }
            )

        return attrs
class AttendanceUpdateSerializer(
    BaseAttendanceSerializer
):
    """
    Serializer for updating attendance records.
    """
    class Meta(BaseAttendanceSerializer.Meta):
        model = Attendance

        fields = (
            "status",
            "remarks",
        )