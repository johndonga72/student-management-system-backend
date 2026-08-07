"""
Custom exceptions for the Tenant module.
"""
class TenantException(Exception):
    """
    Base exception for all tenant-related errors.
    """
    default_message = "Tenant error occurred."

    def __init__(self, message: str | None = None):
        super().__init__(message or self.default_message)


class MissingTenantHeaderException(TenantException):
    """
    Raised when the tenant header is missing.
    """

    default_message = "Tenant code header is required."


class TenantNotFoundException(TenantException):
    """
    Raised when the requested tenant does not exist.
    """

    default_message = "Tenant not found."


class InactiveTenantException(TenantException):
    """
    Raised when the tenant is inactive.
    """

    default_message = "Tenant is inactive."


class InvalidTenantStatusException(TenantException):
    """
    Raised when the tenant is in an invalid state.
    """

    default_message = "Tenant status is invalid."