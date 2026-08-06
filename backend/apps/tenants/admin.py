"""
Admin configuration for the Tenant application.
"""
from django.contrib import admin
from .models import Tenant
@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Tenant model.
    """
    list_display = (
        "id",
        "name",
        "code",
        "email",
        "phone_number",
        "status",
        "is_deleted",
        "created_at",
    )
    list_filter = (
        "status",
        "is_deleted",
        "created_at",
    )
    search_fields = (
        "name",
        "code",
        "email",
        "phone_number",
    )
    ordering = ("-created_at",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            "Tenant Information",
            {
                "fields": (
                    "name",
                    "code",
                    "email",
                    "phone_number",
                    "address",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "status",
                    "is_deleted",
                )
            },
        ),
        (
            "Audit Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        """
        Make tenant code read-only after the tenant has been created.
        """
        readonly_fields = list(super().get_readonly_fields(request, obj))

        if obj:
            readonly_fields.append("code")

        return readonly_fields