"""
Tenant model choice definitions.
This module contains reusable choice classes used by the Tenant
domain models. Keeping choices in a dedicated module improves
maintainability and keeps model files clean.
"""
from django.db import models
class TenantStatus(models.TextChoices):
    """
    Represents the operational status of a tenant.

    Attributes:
        ACTIVE: Tenant is active and can access the platform.
        INACTIVE: Tenant is temporarily inactive.
        SUSPENDED: Tenant has been suspended by the platform.
    """
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    SUSPENDED = "SUSPENDED", "Suspended"
    