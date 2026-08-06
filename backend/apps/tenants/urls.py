from django.urls import path

from apps.tenants.views import (
    TenantAPIView,
    TenantDeleteAPIView,
    TenantListAPIView,
    TenantStatusAPIView,
)

urlpatterns = [
    path(
        "",
        TenantAPIView.as_view(),
        name="tenant-create",
    ),
    path(
        "list/",
        TenantListAPIView.as_view(),
        name="tenant-list",
    ),
    path(
        "<int:tenant_id>/",
        TenantAPIView.as_view(),
        name="tenant-detail",
    ),
    path(
        "<int:tenant_id>/status/",
        TenantStatusAPIView.as_view(),
        name="tenant-status",
    ),
    path(
        "<int:tenant_id>/delete/",
        TenantDeleteAPIView.as_view(),
        name="tenant-delete",
    ),
]