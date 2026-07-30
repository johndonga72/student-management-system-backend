"""
Reusable serializers for the Dashboard module.
"""
from rest_framework import serializers
class AcademicSummarySerializer(serializers.Serializer):
    """
    Academic summary statistics.
    """

    total_students = serializers.IntegerField()
    total_teachers = serializers.IntegerField()
    total_departments = serializers.IntegerField()
    total_courses = serializers.IntegerField()
    total_subjects = serializers.IntegerField()
    
class AttendanceSummarySerializer(serializers.Serializer):
    """
    Attendance summary statistics.
    """
    total_attendance = serializers.IntegerField()
    present_count = serializers.IntegerField()
    absent_count = serializers.IntegerField()
    late_count = serializers.IntegerField()
    attendance_percentage = serializers.FloatField()
class RecentActivitySerializer(serializers.Serializer):
    """
    Recently created records.
    """
    recent_students = serializers.ListField()
    recent_teachers = serializers.ListField()
    recent_subjects = serializers.ListField()