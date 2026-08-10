from django.http import JsonResponse
from apps.tenants.utils import TenantResolver
from apps.tenants.models import Tenant
from apps.tenants.models.choices import TenantStatus
from apps.tenants.exceptions import (
    TenantException,
    MissingTenantHeaderException,
    TenantNotFoundException,
    InactiveTenantException,
    InvalidTenantStatusException,
)
class TenantMiddleware:
    """
    Middleware responsible for resolving the current tenant
    for every incoming request.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        """
        Process each incoming request.
        """

        if self._should_skip_request(request):
            return self.get_response(request)

        try:
            tenant_code = self._extract_tenant_code(request)

            if not tenant_code:
                raise MissingTenantHeaderException()

            tenant = self._get_tenant(tenant_code)

            self._attach_tenant(
                request=request,
                tenant=tenant,
            )

        except TenantException as exc:
            return self._build_error_response(
                message=str(exc),
                status_code=400,
            )

        return self.get_response(request)
        
    def _should_skip_request(self, request) -> bool:
        """
        Determine whether tenant resolution should be skipped
        for the current request.
        """

        skip_prefixes = (
            "/admin/",
            "/static/",
            "/media/",
            "/favicon.ico",
            "/api/v1/schema/",
            "/api/v1/docs/",
            "/redoc/",
            
            
        )

        return request.path.startswith(skip_prefixes)
    
    def _extract_tenant_code(self, request) -> str | None:
        """
        Extract tenant code from the request header.
        """

        return request.headers.get("X-Tenant-Code")
    
    def _get_tenant(
        self,
        tenant_code: str,
    ) -> Tenant:
        """
        Resolve and validate the tenant.
        """

        tenant = TenantResolver.resolve_by_code(
            tenant_code=tenant_code,
        )

        if tenant is None:
            raise TenantNotFoundException()

        if tenant.status == TenantStatus.INACTIVE:
            raise InactiveTenantException()

        if tenant.status != TenantStatus.ACTIVE:
            raise InvalidTenantStatusException()

        return tenant
    
    def _attach_tenant(
        self,
        request,
        tenant: Tenant,
    ) -> None:
        """
        Attach the resolved tenant to the current request.
        """
        request.tenant = tenant

    def _build_error_response(
        self,
        message: str,
        status_code: int,
    ) -> JsonResponse:
        """
        Build a standardized JSON error response.
        """

        return JsonResponse(
            data={
                "success": False,
                "message": message,
            },
            status=status_code,
        )
