# Multi-Tenant Architecture

**Project:** Student Management System

**Version:** 1.0

**Architecture Type:** Shared Database – Shared Schema

---

# 1. Overview

The Student Management System is designed as a **Multi-Tenant Software-as-a-Service (SaaS)** platform that allows multiple educational organizations to use the same application while maintaining complete isolation of their data.

Each educational organization is represented as a **Tenant**, and every tenant manages its own students, teachers, departments, courses, subjects, attendance, examinations, and results independently.

The objective of this architecture is to provide a scalable, secure, and maintainable backend capable of supporting multiple organizations from a single deployment.

---

# 2. Business Requirements

The platform must satisfy the following business requirements:

* One application serves multiple educational organizations.
* Every organization is represented as a Tenant.
* Each tenant owns its own academic and administrative data.
* Users belong to exactly one tenant.
* Users can access only the data of their own tenant.
* Cross-tenant data access is strictly prohibited.
* Every tenant operates independently while sharing the same application instance.
* The application must support future migration to advanced multi-tenant strategies if business requirements evolve.

---

# 3. Business Architecture

```
Platform

│

└── Tenant

      │

      ├── Users

      ├── Departments

      ├── Courses

      ├── Subjects

      ├── Attendance

      ├── Examinations

      ├── Results

      └── Dashboard
```

Each Tenant acts as an independent educational organization inside the platform.

---

# 4. Database Strategy

## Selected Architecture

**Shared Database + Shared Schema**

All tenants share a single PostgreSQL database and a single schema.

Every tenant-owned table stores a direct relationship to the Tenant entity using a `tenant` foreign key.

Example:

```
Department

id

tenant_id

name

status
```

This strategy provides:

* Lower infrastructure cost
* Easier deployment
* Simple migrations
* High maintainability
* Good scalability for small and medium-sized SaaS platforms

---

# 5. Tenant Entity Architecture

The Tenant entity is the root of the entire application.

Relationship hierarchy:

```
Tenant

│

├── Users

├── Departments

├── Courses

├── Subjects

├── Attendance

├── Examinations

├── Result

└── Dashboard


```

Every tenant-owned record maintains a direct relationship with its Tenant.

---

# 6. Request Flow

Every incoming request follows the same lifecycle:

```
Client

↓

JWT Authentication

↓

Tenant Middleware

↓

Tenant Resolution

↓

request.tenant

↓

APIView

↓

Service Layer

↓

Database
```

The Tenant Middleware resolves the tenant before any business logic is executed.

---

# 7. Security and Data Isolation

The following rules guarantee tenant isolation:

* Every authenticated user belongs to exactly one tenant.
* Every tenant-owned record belongs to exactly one tenant.
* Queries must always be filtered using the current tenant.
* Cross-tenant access is prohibited.
* Missing or invalid tenant information results in an immediate error response.
* Tenant resolution occurs before request processing.

---

# 8. Proposed Folder Structure

```
apps/

    tenants/

core/

    middleware/

docs/

    architecture/
```

The Tenant module will contain all tenant-specific business logic, while middleware is responsible for tenant resolution.

---

# 9. Implementation Roadmap

The implementation will follow this order:

1. Create Tenant application
2. Create Tenant model
3. Link CustomUser with Tenant
4. Implement Tenant Middleware
5. Implement Tenant Resolution
6. Add Tenant relationship to tenant-owned models
7. Update Service Layer
8. Perform Multi-Tenant Testing

---

# 10. Future Enhancements

The current architecture has been designed to support future improvements, including:

* Subdomain-based tenant resolution
* Separate schema per tenant
* Separate database per tenant
* Tenant subscription management
* Billing system
* Custom tenant branding
* Tenant-specific analytics
* Audit logging
* Platform administration dashboard

---

# 11. Design Decisions

The following architectural decisions were made during system design:

* Shared Database + Shared Schema was selected to balance simplicity, maintainability, and scalability.
* Every tenant-owned entity stores a direct Tenant relationship.
* Every user belongs to exactly one tenant.
* Tenant resolution is performed using middleware.
* Business logic remains inside the Service Layer.
* API Views remain thin and contain no business logic.
* Tenant isolation is enforced before service execution.

---

# 12. Current Limitations

The current implementation intentionally excludes the following advanced features:

* Multiple database routing
* Schema-per-tenant architecture
* Cross-tenant administrators
* Tenant billing and subscription management
* Automatic tenant provisioning
* White-label customization

These features may be introduced in future versions as the platform evolves.

---

# Conclusion

The selected multi-tenant architecture provides a secure, scalable, and maintainable foundation for the Student Management System. By centralizing tenant resolution, enforcing strict data isolation, and maintaining a clean service-oriented architecture, the platform is well-positioned for future enterprise-level enhancements while remaining simple enough for the current implementation.
