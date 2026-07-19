"""
Department API views.
"""
from .department import (
    DepartmentCreateAPIView,
    DepartmentListAPIView,
    DepartmentDetailAPIView,
    DepartmentStatusAPIView,
    DepartmentDeleteAPIView,
    DepartmentUpdateAPIView,
    
)

__all__ = [
    "DepartmentCreateAPIView",
    "DepartmentListAPIView",
    "DepartmentDetailAPIView",
    "DepartmentStatusAPIView",
    "DepartmentDeleteAPIView",
    "DepartmentUpdateAPIView",
    
]