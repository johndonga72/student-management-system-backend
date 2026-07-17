"""
Business services for department-related operations.
"""
from apps.departments.models import Department
class DepartmentService:
    """
    Service class containing business logic for department operations.
    """
    @staticmethod
    def create_department(validated_data: dict) -> Department:
        """
        Create a new department.
        Args:
            validated_data: Validated department data from the serializer.
        Returns:
            Department: The newly created department instance.
        """
        return Department.objects.create(**validated_data)