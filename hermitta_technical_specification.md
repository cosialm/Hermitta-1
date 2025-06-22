# Hermitta Web System: High-Level Technical Specification

**Version:** 1.0
**Date:** 2025-06-21

## 1. Introduction & System Overview

### 1.1. Purpose
This document provides a high-level technical specification for the Hermitta web system. Hermitta is a comprehensive property management platform designed to facilitate interactions and workflows between Landlords, Tenants, Vendors, and System Administrators. Its core functionalities include property listing, lease management, financial tracking, maintenance request handling, and user management.

### 1.2. Scope
This specification covers the technical architecture, backend and frontend design guidelines, database schema considerations, API design principles, security requirements, and key non-functional requirements. It is intended for developers, architects, and project managers involved in the development of the Hermitta system.

### 1.3. Target Users
*   **Landlords/Property Managers:** Manage properties, leases, tenants, finances, and maintenance.
*   **Tenants:** View lease details, make payments, submit maintenance requests, communicate with landlords.
*   **Vendors:** Receive job assignments, submit quotes and invoices, manage their service profile.
*   **System Administrators:** Manage users, system configurations, and oversee platform operations.
*   **Public Users (Unregistered):** Browse property listings and platform information.

## 2. System Architecture

### 2.1. Architectural Style
A **Monolithic Application with a Service-Oriented Backend** is proposed for the initial development, deployed as a single unit but with internally organized services for different domains (User, Property, Lease, etc.). The frontend will be a **Single Page Application (SPA)**.

### 2.2. Technology Stack (Recommended)
*   **Backend:**
    *   **Language:** Python (3.9+)
    *   **Framework:** Flask (with Blueprints for modularity)
    *   **ORM:** SQLAlchemy (with Flask-SQLAlchemy)
    *   **Database Migrations:** Flask-Migrate (Alembic)
    *   **Authentication:** JWT-based for API anuthentication. Flask-Login could be considered for initial session management if server-side rendering is partially used, but JWT is preferred for SPA.
    *   **Task Queue (Future Consideration):** Celery with Redis/RabbitMQ for background tasks (e.g., sending notifications, processing reports).
*   **Frontend:**
    *   **Framework:** Modern JavaScript framework (e.g., React, Vue.js, or Angular - developer/team choice, must be justified).
    *   **State Management:** Appropriate library for the chosen framework (e.g., Redux/Zustand for React, Vuex/Pinia for Vue).
    *   **Styling:** CSS-in-JS, CSS Modules, or a utility-first framework like Tailwind CSS.
*   **Database:**
    *   **Development:** SQLite
    *   **Production:** PostgreSQL (recommended for scalability and features)
*   **Web Server (Production):** Gunicorn or uWSGI behind a reverse proxy like Nginx.
*   **Deployment (Future Consideration):** Docker, Kubernetes, or PaaS (e.g., Heroku, AWS Elastic Beanstalk).

### 2.3. High-Level Diagram
*(A diagram would typically be here showing: Client (Browser) -> Frontend SPA -> API Gateway (Optional) -> Backend API (Flask App) -> Services -> Database. Also showing external services like Email, SMS, Payment Gateways).*

## 3. Backend Specification

### 3.1. Core Principles
*   **Service-Oriented Design:** Business logic encapsulated within service classes (e.g., `UserService`, `PropertyService`, `LeaseService`). Services interact with models and are called by route handlers.
*   **Modularity:** Use Flask Blueprints to organize routes by domain (e.g., `auth`, `users`, `properties`, `leases`).
*   **Stateless API:** API endpoints should be stateless; session state primarily managed by the client using tokens.
*   **Comprehensive Testing:** Unit tests for models and services; integration tests for API endpoints.
*   **Configuration Management:** Environment-specific configurations using `config.py` and environment variables.

### 3.2. Key Backend Modules (refer to existing codebase structure)
*   **`hermitta_app/`:** Main application package.
    *   `__init__.py`: App factory (`create_app`), extension initialization (SQLAlchemy, Migrate).
    *   `models/`: SQLAlchemy model definitions.
    *   `services/`: Business logic layer.
    *   `routes/`: API endpoint definitions (Blueprints).
    *   `utils/` (optional): Helper functions, common utilities.
*   **`config.py`:** Configuration classes.
*   **`run.py`:** Application entry point for running the development server.
*   **`migrations/`:** Alembic database migration scripts.

### 3.3. Database Schema
*   Refer to the SQLAlchemy models defined in the `models/` directory of the existing codebase. These include:
    *   `User`: Stores user data, roles (Landlord, Tenant, Vendor, Admin, Staff), authentication details (password hash, MFA), role-specific fields (KRA PIN, vendor services), consent.
    *   `Property`: Property details, type, status, amenities, location data.
    *   `Lease`: Lease terms, links to property, landlord, tenant(s), financial details, document links.
    *   `FinancialTransaction`: Income/expense tracking, categorization, recurrence.
    *   `Payment`: Records of payments made, status, gateway details.
    *   `GatewayTransaction`: Detailed logs of interactions with payment gateways.
    *   `MaintenanceRequest`: Details of maintenance issues, status, assignment, quotes, invoices.
    *   `Document`, `DocumentFolder`, `DocumentShare`: For file management and sharing.
    *   `Notification`, `NotificationTemplate`: For user notifications.
    *   Configuration Models: `LandlordApplicationConfig`, `LandlordGatewayConfig`, `LandlordMpesaConfig`, `LandlordReminderRule`, `SyndicationPlatform`.
    *   `AuditLog`: For tracking significant system events.
    *   Supporting models: `Quote`, `VendorInvoice`, `RentalApplication`, `ApplicationScreening`, etc.
*   **Relationships:** All relationships (one-to-one, one-to-many, many-to-many) are defined within the SQLAlchemy models using `db.relationship` and `db.ForeignKey`.
*   **Indexes:** Ensure appropriate database indexes are defined on frequently queried columns (especially foreign keys, email, phone_number, status fields, dates).

### 3.4. API Design (RESTful)
*   **General Principles:**
    *   Use standard HTTP methods (GET, POST, PUT, DELETE, PATCH).
    *   Use clear, resource-oriented URLs (e.g., `/users`, `/users/<id>`, `/properties/<property_id>/leases`).
    *   Use JSON for request and response bodies.
    *   Implement consistent error handling and status codes (e.g., 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error).
    *   Support pagination for list endpoints (e.g., `?page=1&per_page=20`).
    *   Support filtering and sorting via query parameters for list endpoints.
*   **Authentication & Authorization:**
    *   JWTs for authenticating API requests. Token sent in `Authorization: Bearer <token>` header.
    *   Role-based and ownership-based authorization enforced at the service or route level for all sensitive operations.
*   **Key API Endpoint Groups (refer to `hermitta_frontend_conceptual_framework_v2.md` Section 6 & 7 for detailed mapping):**
    *   `/auth/*`: User registration, login, password reset, MFA.
    *   `/users/*`: User profile management, admin user CRUD.
    *   `/properties/*`: Public property listings, landlord property CRUD.
    *   `/leases/*`: Lease management.
    *   `/financial-transactions/*`, `/payments/*`, `/budgets/*`: Financial operations.
    *   `/maintenance-requests/*`, `/quotes/*`, `/vendor-invoices/*`: Maintenance workflows.
    *   `/rental-applications/*`, `/application-screenings/*`: Application processing.
    *   `/documents/*`, `/document-folders/*`, `/document-shares/*`: Document handling.
    *   `/notifications/*`, `/notification-templates/*`: Notification system.
    *   `/landlord-configs/*`: Landlord-specific settings.
    *   `/admin/*`: Admin-specific operations (system config, audit logs).

## 4. Frontend Specification

### 4.1. Core Principles
*   **Component-Based Architecture:** Build the UI using reusable components.
*   **SPA (Single Page Application):** Provides a fluid user experience without full page reloads for most interactions.
*   **Responsive Design:** Ensure usability across desktop, tablet, and mobile devices.
*   **Accessibility (a11y):** Adhere to WCAG guidelines where feasible.
*   **Clear State Management:** Use a predictable state management pattern.
*   **API Integration:** All dynamic content and actions are driven by the backend API. Graceful handling of API errors and loading states.

### 4.2. Key Frontend Components
*   Refer to the `hermitta_frontend_conceptual_framework_v2.md` document for a detailed breakdown of:
    *   Public Area Components (Homepage, Property Listings, Property Details).
    *   Authentication Components (Sign Up, Sign In, MFA, Password Reset, Profile).
    *   Role-Specific Dashboard Components (Landlord, Tenant, Admin, Staff, Vendor).
    *   Cross-Cutting Components (Forms, Tables, Modals, Notifications, Search/Filter).

### 4.3. User Experience (UX) Guidelines
*   **Intuitive Navigation:** Users should easily find what they need.
*   **Consistent UI:** Similar actions and information should be presented consistently across the platform.
*   **Feedback:** Provide immediate feedback for user actions (e.g., success messages, loading indicators, error notifications).
*   **Minimize Friction:** Streamline common tasks, especially registration and core workflows.
*   **Role-Tailored Experience:** Dashboards and available actions should be clearly tailored to the logged-in user's role.

## 5. Security Considerations

*   **Authentication:** Secure password hashing (e.g., bcrypt, Argon2). Secure JWT handling (short expiry for access tokens, refresh tokens). Implement MFA (TOTP).
*   **Authorization:** Robust role-based access control (RBAC) and ownership checks on all backend operations. Prevent unauthorized data access or modification.
*   **Input Validation:** Validate and sanitize all user inputs on both frontend and backend (to prevent XSS, SQLi, etc.).
*   **Data Protection:**
    *   Encrypt sensitive data at rest where appropriate (e.g., KRA PINs, certain vendor verification details if stored long-term).
    *   Use HTTPS for all communication.
    *   Adhere to data privacy principles (e.g., GDPR, Kenyan Data Protection Act).
*   **API Security:** Protect against common API vulnerabilities (e.g., insecure direct object references, rate limiting on sensitive endpoints).
*   **Dependency Management:** Keep all libraries and frameworks up-to-date to patch known vulnerabilities.
*   **Audit Logging:** Comprehensive logging of significant user actions and system events (as per `AuditLog` model).

## 6. Non-Functional Requirements

*   **Performance:**
    *   API response times should generally be <500ms for common operations.
    *   Frontend page load times should be optimized.
    *   Efficient database queries, use of indexing.
*   **Scalability (Future):** While initially monolithic, the service-oriented backend structure should allow for future scaling of individual components if needed. Database choice (PostgreSQL) supports scalability.
*   **Reliability/Availability:** Aim for high uptime. Implement robust error handling and logging.
*   **Maintainability:** Clean, well-documented, and modular code (both backend and frontend). Adherence to coding standards (e.g., PEP 8 for Python).
*   **Testability:** High unit and integration test coverage for the backend. Frontend component/unit tests are encouraged.

## 7. Deployment & Operations (High-Level)

*   **Environments:** Development, Staging, Production.
*   **Version Control:** Git (e.g., GitHub, GitLab).
*   **CI/CD (Future Consideration):** Automated testing and deployment pipelines.
*   **Logging & Monitoring (Production):** Centralized logging (e.g., ELK stack, Sentry) and application performance monitoring.

## 8. Future Considerations (Post-MVP)

*   Advanced reporting and analytics.
*   Full e-signature integration with a third-party provider.
*   Native mobile applications.
*   Advanced AI/ML features (e.g., property valuation, personalized recommendations).
*   Public Vendor Marketplace with direct tenant/homeowner engagement.
*   Expanded payment gateway options.
*   Full i18n/l10n support.

This document provides the guiding technical principles and high-level specifications. Detailed design for individual modules, components, and specific API contracts will be elaborated during the development sprints.
---

This document should give "Rok AI" or any development team a solid, high-level, yet specific technical foundation to start building Hermitta. Remember to also provide the `hermitta_frontend_conceptual_framework_v2.md` file alongside this.
