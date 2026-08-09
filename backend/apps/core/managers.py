from django.db import models
class TenantAwareQuerySet(models.QuerySet):
    """
    QuerySet providing tenant-scoped database operations.
    """
    def for_tenant(self, tenant):
        """
        Return records belonging to the specified tenant.
        """

        return self.filter(tenant=tenant)
    
class TenantAwareManager(models.Manager):
    """
    Manager for tenant-aware models.
    """

    def get_queryset(self):
        return TenantAwareQuerySet(
            self.model,
            using=self._db,
        )
    def for_tenant(self, tenant):
        """
        Return records belonging to the specified tenant.
        """
        return self.get_queryset().for_tenant(tenant)