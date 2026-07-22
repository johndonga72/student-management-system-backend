"""
Base serializer for student validations.
"""
from django.utils import timezone
from rest_framework import serializers
from apps.students.models import Student
class BaseStudentSerializer(serializers.ModelSerializer):
    """
    Base serializer containing reusable validation logic.
    """
    class Meta:
        model = Student
        fields = "__all__"
    def validate_phone(self, value: str) -> str:
        """
        Validate student phone number.
        """
        if len(value) != 10 or not value.isdigit():
            raise serializers.ValidationError(
                "Phone number must contain exactly 10 digits."
            )
        return value
    def validate_guardian_phone(self, value: str) -> str:
        """
        Validate guardian phone number.
        """
        if len(value) != 10 or not value.isdigit():
            raise serializers.ValidationError(
                "Guardian phone number must contain exactly 10 digits."
            )
        return value
    def validate_date_of_birth(self, value):
        """
        Validate date of birth.
        """
        if value >= timezone.now().date():
            raise serializers.ValidationError(
                "Date of birth must be in the past."
            )
        return value