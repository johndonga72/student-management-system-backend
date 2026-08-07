from typing import Optional
from apps.tenants.models import Tenant
class TenantResolver:
    """
    Centralized utility for resolving tenant information.

    This class contains reusable tenant lookup strategies
    used throughout the application.
    """
    @staticmethod
    def resolve_by_code(
        tenant_code: str,
    ) -> Optional[Tenant]:
        """
        Resolve tenant using tenant code.
        """
        return Tenant.objects.filter(
            code=tenant_code,
            is_deleted=False,
        ).first()