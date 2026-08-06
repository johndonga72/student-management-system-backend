from rest_framework import serializers
from apps.results.models import Result
class BaseResultSerializer(serializers.ModelSerializer):
    """
    Base serializer for Result model.
    """
    class Meta:
        model = Result
        fields = [
            "id",
            "student",
            "examination",
            "obtained_marks",
            "result_status",
            "exam_type",
            "exam_date",
            "academic_year",
            "remarks",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "result_status",
            "created_at",
            "updated_at",
        ]