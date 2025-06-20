# Functional Overview - Kenyan Rental Management System

This document provides a high-level overview of the system's functionalities, broken down by user roles and key modules. It is intended to align understanding of the system's capabilities across different stakeholders.

## I. Landlord Role - Functional Breakdown

This section details the features and functionalities available to users with the "Landlord" role.

### I. Property Management
(Details as previously defined)
### II. Tenant Management
(Details as previously defined)
### III. Lease Management
(Details as previously defined)
### IV. Financial Management
(Details as previously defined)
### V. Maintenance Management
(Details as previously defined)
### VI. Communication
(Details as previously defined)
### VII. Reporting (Access to Predefined Reports)
(Details as previously defined)
### VIII. Vendor/Staff Management
(Details as previously defined)
### IX. Account Settings & Configuration
(Details as previously defined)

---
## II. Tenant Role - Functional Deep Dive

This section details the features and functionalities available to users with the "Tenant" role.

### I. Account Management & Profile
(Details as previously defined)
### II. Property & Lease Information
(Details as previously defined)
### III. Rent Payments
(Details as previously defined)
### IV. Maintenance Requests
(Details as previously defined)
### V. Communication with Landlord/Property Manager
(Details as previously defined)

---
## III. Vendor/Service Provider Role - Functional Deep Dive

This section details the features and functionalities available to users with the "Vendor" or "Service Provider" role (Phase 6+).

### I. Account Management & Profile
(Details as previously defined)
### II. Job Management (Maintenance Requests)
(Details as previously defined)
### III. Quote Management
(Details as previously defined)
### IV. Work Completion & Attachments
(Details as previously defined)
### V. Invoice Management
(Details as previously defined)
### VI. Communication (Job-Specific)
(Details as previously defined)

---
## IV. Staff Role (Property Manager Staff/Accountant) - Functional Deep Dive

This section details features for users with "STAFF" or "ACCOUNTANT" roles (Phase 6+). Staff access is governed by `staff_permissions` set by the Landlord or Admin, determining which properties they can manage and what actions they can perform (e.g., view-only vs. edit for financials, ability to assign vendors, communicate with tenants).

### I. Account Management & Profile
(Details as previously defined)
### II. Property & Tenant Management (Permission-Dependent)
(Details as previously defined)
### III. Lease Management (Permission-Dependent)
(Details as previously defined)
### IV. Financial Management (Permission-Dependent, esp. for 'ACCOUNTANT' role)
(Details as previously defined)
### V. Maintenance Management (Permission-Dependent)
(Details as previously defined)
### VI. Communication (Permission-Dependent)
(Details as previously defined)
### VII. Reporting (Access based on permissions)
(Details as previously defined)

---
## V. System Administrator Role (Platform Admin) - Functional Deep Dive

This section details features for users with the "ADMIN" role, responsible for overall platform management, health, and integrity. Access to these functions is highly privileged.

### I. User Account Management (Platform Level)
(Details as previously defined)
### II. Platform Configuration & Management
(Details as previously defined)
### III. System Health Monitoring & Support
(Details as previously defined)
### IV. Security & Compliance Management
(Details as previously defined)
### V. Financial Oversight (Platform Level - if applicable)
(Details as previously defined)

---
## VII. Cross-Cutting Considerations & Future Refinements

This section notes important system-wide considerations and areas for potential future development that impact multiple roles and modules.

### 1. Audit Logging
A dedicated `AuditLog` model has been conceptualized to track significant user actions (especially by Landlords for sensitive changes like M-Pesa configurations, lease modifications, and financial entries) and all System Administrator actions. This is crucial for security, accountability, and troubleshooting. Key events to log include, but are not limited to:
*   User authentication events (logins, logouts, password changes, MFA updates).
*   Creation, modification, and deletion of major data entities (Properties, Leases, Payments, Financial Transactions, Maintenance Requests, User Accounts by Admin).
*   Changes to critical configurations (e.g., `LandlordMpesaConfiguration`, `LandlordReminderRule`, `SyndicationPlatform` settings by Admin).
*   Access to or export of sensitive data (e.g., PII reports by Admin for DSAR).
*   Key security events (e.g., authorization failures, suspicious M-Pesa callback validation failures).
The `AuditLog` will capture who performed the action (`user_id`), when (`timestamp`), the type of action (`action_type`), the affected entity (`target_entity_type`, `target_entity_id`), details of changes (`details_before`, `details_after` where feasible), and contextual information like IP address and user agent.

### 2. Admin-Specific API Endpoints
The functionalities listed for the System Administrator role will require a dedicated set of API endpoints, typically namespaced (e.g., under an `/api/v1/admin/...` path). These endpoints must be protected with strict authorization, ensuring only users with the 'ADMIN' role (or other specifically designated privileged roles) can access them. These admin APIs will facilitate:
*   User management (viewing, activating/deactivating, modifying roles, assisting with lockouts).
*   Platform-wide configuration management (e.g., default notification templates, system settings, `SyndicationPlatform` management).
*   System monitoring and health check access.
*   Compliance actions, such as servicing Data Subject Access Requests (DSAR) by exporting or managing user data.
*   Access to comprehensive audit logs.

### 3. Staff Permission Logic Implementation
The `staff_permissions` JSON field on the `User` model (for 'STAFF' and 'ACCOUNTANT' roles) provides flexibility for Landlords or Admins to define what these users can do on their behalf. The API implementation will need robust and consistent logic (e.g., through middleware, decorators, or service-layer checks) to parse these permissions for every relevant request. This ensures Staff users can only access data (e.g., specific properties, leases, financial records) and perform actions (e.g., view, edit, create, delete, assign vendors, communicate) within the scope explicitly granted to them by their supervising Landlord or a System Administrator. This is crucial for maintaining data segregation and enforcing the principle of least privilege for staff accounts.
