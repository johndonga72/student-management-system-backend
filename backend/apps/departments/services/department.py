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
    @staticmethod
    def list_departments():
        """
        Retrieve all active departments.

        Returns:
            QuerySet[Department]: A queryset of active departments.
        """
        return Department.objects.filter(
            is_active=True
        ).order_by("name")
    
    @staticmethod
    def get_department_by_id(department_id: int) -> Department:
            """
            Retrieve a department by its ID.

            Args:
                department_id: Department primary key.

            Returns:
                Department: Department instance.

            Raises:
                Department.DoesNotExist:
                    If the department does not exist.
            """
            return Department.objects.get(
                id=department_id,
                is_active=True,
            )
    @staticmethod
    def update_department(
        department_id: int,
        validated_data: dict,
    ) -> Department:
        """
        Update an existing department.
        """
        department = DepartmentService.get_department_by_id(
            department_id
        )

        for field, value in validated_data.items():
            setattr(department, field, value)

        department.save()

        return department 
    @staticmethod
    def change_department_status(
        department_id: int,
        is_active: bool,
    ) -> Department:
        """
        Activate or deactivate a department.
        """
        department = DepartmentService.get_department_by_id(
            department_id
        )
        department.is_active = is_active
        department.save(update_fields=["is_active", "updated_at"])
        return department
    @staticmethod
    def delete_department(
        department_id: int,
    ) -> None:
        """
        Soft delete a department.
        """
        department = DepartmentService.get_department_by_id(
            department_id
        )
        department.is_active = True
        department.save(update_fields=["is_active", "updated_at"])
        