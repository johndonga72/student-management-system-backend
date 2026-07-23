"""
Student view exports.
This module exposes the public API views for the
student management module.
"""
from .student import (
    StudentApprovalAPIView,
    StudentDeleteAPIView,
    StudentListAPIView,
    StudentProfileAPIView,
    StudentStatusAPIView,
)
__all__ = [
    "StudentProfileAPIView",
    "StudentListAPIView",
    "StudentApprovalAPIView",
    "StudentStatusAPIView",
    "StudentDeleteAPIView",
]