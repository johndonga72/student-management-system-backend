from drf_spectacular.utils import OpenApiParameter


def add_tenant_header(result, generator, request, public):
    """
    Add X-Tenant-Code to every API operation.
    """

    tenant_parameter = {
        "name": "X-Tenant-Code",
        "in": "header",
        "required": True,
        "schema": {
            "type": "string",
        },
        "description": (
            "Tenant code used to resolve "
            "the current tenant."
        ),
    }

    for path_data in result["paths"].values():
        for operation in path_data.values():

            if not isinstance(operation, dict):
                continue

            parameters = operation.setdefault(
                "parameters",
                [],
            )

            # Avoid duplicates
            if not any(
                parameter.get("name") == "X-Tenant-Code"
                and parameter.get("in") == "header"
                for parameter in parameters
            ):
                parameters.append(
                    tenant_parameter
                )

    return result