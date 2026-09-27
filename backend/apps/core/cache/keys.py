"""Cache-key definitions for the Student ERP.

This module centralizes cache-key construction so that cache keys
remain consistent across the application.

Cache keys must include tenant-specific identifiers whenever the
cached data belongs to a particular tenant.
"""

from __future__ import annotations

class DepartmentCacheKeys:
    """Cache-key builders for the Department module."""

    @staticmethod
    def list(
        tenant_id: int,
    ) -> str:
        """Return the cache key for a tenant's department list.

        Args:
            tenant_id: Primary-key ID of the current tenant.

        Returns:
            Tenant-specific department-list cache key.
        """
        return (
            f"department:list:"
            f"tenant:{tenant_id}"
        )