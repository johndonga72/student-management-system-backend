"""
Custom permission classes for role-based authorization.
"""
from rest_framework.permissions import BasePermission
from apps.accounts.models import UserRole
class IsAdminRole(BasePermission):
    """
    Allows access only to users with the ADMIN role.
    """
    message = "You do not have permission to perform this action."
    def has_permission(self, request, view):
        """
        Check whether the authenticated user has the ADMIN role.
        """
        return (
            request.user.is_authenticated
            and request.user.role == UserRole.ADMIN
        )
