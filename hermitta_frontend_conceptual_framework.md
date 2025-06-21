# Hermitta Application: Frontend Conceptual Framework

## 1. Introduction

This document outlines the conceptual framework for the Hermitta application's frontend. It details the high-level structure, navigation, key components, user flows, and anticipated API interaction points. This framework is intended to guide frontend developers in building a user interface that is consistent, user-friendly, and tightly integrated with the backend services.

## 2. High-Level Application Structure

The application is broadly divided into two main sections:

*   **Public Area (Pre-Login):** Accessible to all visitors. Focuses on property discovery, platform information, and user onboarding (Sign Up/Sign In).
*   **Authenticated Area (Post-Login - User Dashboards):** Requires user authentication. Provides role-specific dashboards and functionalities for Landlords, Tenants, Administrators, Staff, and Vendors.

## 3. Primary Navigation

### 3.1. Public Navigation (Pre-Login)

*   **Location:** Typically a top navigation bar.
*   **Elements:**
    *   **Logo/Homepage Link:** (e.g., "Hermitta") -> Navigates to `/`.
    *   **Properties / Vacancies:** -> Navigates to property listings page (e.g., `/properties`).
    *   **About Us:** (Optional static page).
    *   **Contact Us:** (Optional static page/form).
    *   **Sign In:** -> Navigates to Login page (e.g., `/auth/login`).
    *   **Sign Up:** -> Navigates to Registration page (e.g., `/auth/register`).

### 3.2. Authenticated User Navigation (Post-Login)

*   **Layout:** Typically a combination of a persistent sidebar (for main sections) and a top bar (for user profile, notifications).
*   **Common Top Bar Elements (Most Roles):**
    *   **Logo/Dashboard Home Link.**
    *   **Notifications Icon/Link:** Access to user's notifications.
    *   **User Profile Dropdown/Link:**
        *   My Profile / Account Settings.
        *   Sign Out.
*   **Sidebar Navigation (Role-Specific):**

    *   **Landlord:**
        *   Dashboard Overview
        *   Properties (Manage properties, units)
        *   Leases (Manage leases, templates, amendments)
        *   Tenants (View tenants, communication history)
        *   Financials (Transactions, payments, bank accounts, reports, budgets)
        *   Maintenance (Requests, assignments)
        *   Applications (Rental applications, screening)
        *   Documents (File management)
        *   Communications (Centralized messaging/announcements)
        *   Settings (Application config, payment gateways, reminders, syndication)
    *   **Tenant:**
        *   Dashboard Overview
        *   My Lease (Details, documents)
        *   Payments (History, make payments)
        *   Maintenance (Submit & track requests)
        *   Messages (Communication with landlord/staff)
        *   My Documents (Shared documents)
    *   **Admin:**
        *   System Overview
        *   User Management (All roles)
        *   Property Oversight (All properties)
        *   Financial Oversight (System-wide)
        *   System Configuration (Notification templates, global settings)
        *   Audit Logs
    *   **Staff:**
        *   Navigation dynamically rendered based on `staff_permissions`.
        *   Potential items: Assigned Properties, Tasks, Maintenance, Applications, etc.
    *   **Vendor:**
        *   Dashboard Overview
        *   Assigned Jobs
        *   Quotes
        *   Invoices
        *   My Profile/Services
        *   Communication (Job-related)

### 3.3. Footer Navigation (Common)

*   Copyright Information
*   Terms of Service
*   Privacy Policy
*   Contact Us
*   FAQ (Optional)

## 4. User Authentication Components

### 4.1. Sign Up / Registration
*   **Route (Example):** `/auth/register`
*   **Purpose:** New user account creation.
*   **Key Inputs:** First Name, Last Name, Email, Phone, Password, Password Confirmation, Role (Tenant/Landlord).
    *   Conditional Inputs (based on role): KRA PIN (Landlord), Company Name, Services Offered (Vendor - if self-registration is supported).
*   **Key Actions:** Submit form, Link to Sign In.
*   **Primary API Interaction:** `POST /auth/register`
    *   *Payload:* All form data.
    *   *Success:* Message, potential auto-login or redirect to email/phone verification step.
    *   *Failure:* Display errors (e.g., email exists, invalid data).
*   **Secondary API (Suggested):** `POST /auth/check-availability` for real-time email/phone validation.

### 4.2. Sign In / Login
*   **Route (Example):** `/auth/login`
*   **Purpose:** Existing user authentication.
*   **Key Inputs:** Identifier (Email or Phone), Password.
*   **Key Actions:** Submit form, "Forgot Password?" link, Link to Sign Up.
*   **Primary API Interaction:** `POST /auth/login`
    *   *Payload:* `{ "identifier": "...", "password": "..." }`
    *   *Success:* Auth token (JWT), user details (incl. role, MFA status). Redirect to role-specific dashboard or MFA challenge.
    *   *Failure:* Display error ("Invalid credentials").

### 4.3. MFA Challenge
*   **Route (Example):** `/auth/mfa-challenge` (Shown conditionally after login)
*   **Purpose:** Second-factor authentication.
*   **Key Inputs:** OTP Code.
*   **Key Actions:** Verify Code, Use Backup Code.
*   **Primary API Interaction:** `POST /auth/verify-mfa` (Suggested)
    *   *Payload:* `{ "otp_code": "..." }` (requires user context from previous step).
    *   *Success:* Auth token, user details. Redirect to dashboard.
    *   *Failure:* Display error.

### 4.4. Password Reset Request
*   **Route (Example):** `/auth/forgot-password`
*   **Purpose:** Initiate password reset process.
*   **Key Inputs:** Registered Email or Phone Number.
*   **Key Actions:** Send Reset Link/Code.
*   **Primary API Interaction:** `POST /auth/request-password-reset`
    *   *Payload:* `{ "email_or_phone": "..." }`
    *   *Success:* Confirmation message.
    *   *Failure:* Error if account not found.

### 4.5. Password Reset
*   **Route (Example):** `/auth/reset-password?token=<reset_token>`
*   **Purpose:** Set a new password using a valid token.
*   **Key Inputs:** New Password, Confirm New Password. (Token usually from URL).
*   **Key Actions:** Reset Password.
*   **Primary API Interaction:** `POST /auth/reset-password/<token>`
    *   *Payload:* `{ "new_password": "..." }`
    *   *Success:* Confirmation, redirect to login.
    *   *Failure:* Error (invalid/expired token, weak password).

### 4.6. User Profile Management (Post-Login)
*   **Route (Example):** `/profile`, `/settings/profile`
*   **Purpose:** View and update user information.
*   **Sections:** Personal Info, Security (Password Change, MFA Management), Role-Specific Info, Consent.
*   **Key API Interactions:**
    *   `GET /users/profile` (Fetch current user data).
    *   `PUT /users/profile` (Update user data).
    *   `POST /auth/change-password` (Suggested).
    *   MFA Endpoints (Suggested): `POST /auth/setup-mfa`, `POST /auth/verify-mfa-setup`, `POST /auth/disable-mfa`, `GET /auth/mfa-backup-codes`.
    *   Phone Verification: `POST /auth/send-phone-otp`, `POST /auth/verify-phone-otp` (Suggested).

## 5. Public-Facing Components (Pre-Login)

### 5.1. Homepage
*   **Route (Example):** `/`
*   **Purpose:** Entry point, overview, main CTAs.
*   **Key Sections:** Hero, Simplified Search, Featured Properties, How It Works, Value Proposition.
*   **Key API Interactions:** `GET /properties/public?featured=true` (or similar for featured listings).

### 5.2. Property Listings Page
*   **Route (Example):** `/properties`, `/vacancies`
*   **Purpose:** Browse, search, filter available properties.
*   **Key Features:** Advanced Search & Filter Bar (Location, Type, Price, Beds/Baths, Amenities, Sort), Map View, List/Grid View of Property Cards, Pagination.
*   **Property Card (Reusable):** Image, address, price (indicative), beds/baths, type, link to details.
*   **Key API Interactions:** `GET /properties/public` (with extensive query parameters for filtering, sorting, pagination), `GET /properties/public/filter-options` (suggested, for populating filter dropdowns).

### 5.3. Property Details Page
*   **Route (Example):** `/properties/<property_slug_or_id>`
*   **Purpose:** Comprehensive information about a single property.
*   **Key Sections:** Title, Image Gallery, Key Info (Price, Beds/Baths, etc.), Description, Amenities, Location (Map), Contact/Inquiry Form or "Apply Now" CTA.
*   **Key API Interactions:** `GET /properties/public/<id_or_slug>`, `POST /prospect-inquiries` (suggested, for inquiry form).

## 6. User-Specific Dashboard Components (Post-Login)

*(This section details key components for each role. Many will reuse cross-cutting components like tables, forms, and modals.)*

### 6.1. Common Dashboard Elements
*   **Dashboard Wrapper/Layout:** Sidebar navigation, top bar (logo, notifications, user menu).
*   **Overview/Summary Component:** Role-specific KPIs and quick links. (Multiple API calls).
*   **Notifications Component:** List, filters, actions. (API: `GET/PUT /notifications/`).

### 6.2. Landlord Dashboard
*   **Property Management:**
    *   List: `GET /properties/landlord` (or `/properties?landlord_id=self`).
    *   Create/Update/Delete: `POST/PUT/DELETE /properties[/<id>]`.
    *   Units: `GET/POST /properties/<id>/units`, `PUT/DELETE /units/<unit_id>`.
*   **Lease Management:**
    *   List: `GET /leases/landlord` (or `/leases?landlord_id=self`).
    *   Create/Update/View: `POST/PUT/GET /leases[/<id>]`.
    *   Templates: CRUD via `/lease-templates[/<id>]`.
    *   Amendments: CRUD via `/leases/<lease_id>/amendments[/<id>]`.
*   **Tenant Management:**
    *   List: `GET /users/landlord/tenants` (new endpoint or derived from leases).
    *   View: `GET /users/<id>` (or restricted view).
*   **Financial Management:**
    *   Transactions: CRUD via `/financial-transactions?landlord_id=self`.
    *   Payments: `GET /payments?landlord_id=self`.
    *   Bank Accounts: CRUD via `/landlord-bank-accounts[/<id>]`.
    *   Reports: `GET /reports/<type>?landlord_id=self`.
    *   Budgets: CRUD via `/budgets?landlord_id=self`.
*   **Maintenance Management:**
    *   List: `GET /maintenance-requests?landlord_id=self`.
    *   View/Update: `GET/PUT /maintenance-requests/<id>`.
*   **Rental Application Management:**
    *   List: `GET /rental-applications?landlord_id=self`.
    *   View/Update: `GET/PUT /rental-applications/<id>`.
    *   Documents: `GET /rental-applications/<id>/documents`.
    *   Screening: `POST/GET /application-screenings[/<app_id>]`.
*   **Document Management:**
    *   Folders: CRUD via `/document-folders[/<id>]`.
    *   Documents: CRUD via `/documents[/<id>]`, `POST /documents/upload`.
    *   Sharing: `POST/DELETE /document-shares[/<id>]`.
*   **Settings:**
    *   Application Config: `GET/PUT /landlord-configs/application`.
    *   Payment Gateways: `GET/PUT /landlord-configs/(mpesa|gateway)`.
    *   Reminder Rules: CRUD via `/landlord-configs/reminder-rules[/<id>]`.
    *   Syndication: `GET/PUT /landlord-configs/syndication`.

### 6.3. Tenant Dashboard
*   **My Lease:** `GET /leases/tenant/current` (new), `GET /documents/<id>`.
*   **Payments:** `GET /payments/tenant` (new), `POST /payments`.
*   **Maintenance Requests:** `GET /maintenance-requests/tenant` (new), `POST /maintenance-requests`, `GET/PUT /maintenance-requests/<id>`.
*   **Messages:** `GET/POST /messages/...` (robust API needed).
*   **My Documents:** `GET /documents/shared-with-me` (new).

### 6.4. Admin Dashboard
*   **User Management:** `GET/POST/PUT/DELETE /users[/<id>]`.
*   **System Configuration:**
    *   Notification Templates: CRUD via `/notification-templates[/<id>]`.
    *   Syndication Platforms: CRUD via `/syndication-platforms[/<id>]`.
*   **Audit Log Viewer:** `GET /audit-logs` (with filters).

### 6.5. Staff Dashboard
*   Uses subset of Landlord/Admin APIs. Backend authorization is key.
*   Frontend UI elements dynamically rendered based on permissions fetched from e.g. `GET /users/me/permissions`.

### 6.6. Vendor Dashboard
*   **Assigned Jobs:** `GET /maintenance-requests/vendor/assigned` (new) or filtered main list.
*   **Job Details/Updates:** `GET/PUT /maintenance-requests/<id>`.
*   **Quotes:** `POST /quotes`, `GET /quotes/vendor` (new).
*   **Invoices:** `POST /vendor-invoices`, `GET /vendor-invoices/vendor` (new).
*   **Profile:** `GET/PUT /users/profile`.

## 7. Cross-Cutting Components

These components are reused across multiple views and dashboards.

*   **Search & Filtering Bars:** Configurable component using GET params to list endpoints.
*   **Forms:** Base component for layout, validation, submission (POST/PUT to entity endpoints).
*   **Modals/Popups:** For confirmations, quick views, short forms.
*   **Notification Displays:** Toasts, in-app center. (GET `/notifications`, PUT to mark read).
*   **Data Tables/Grids:** Display lists with sorting, pagination, row actions. (GET to list endpoints).
*   **File Uploaders:** `POST multipart/form-data` to upload endpoints (e.g., `/documents/upload`).
*   **WYSIWYG Editor (Optional):** For rich text fields.
*   **Date/Time Pickers:** Standardized date/time selection.

## 8. General Frontend Considerations

*   **State Management:** Choose a robust state management solution (e.g., Redux, Zustand, Vuex, Pinia, or context APIs depending on framework) to manage application-wide state like authenticated user, roles, permissions, notifications, and potentially cached data.
*   **API Service Layer:** Abstract API calls into a dedicated service layer/module on the frontend to keep components clean and make API interactions reusable and manageable.
*   **Responsiveness:** All components must be responsive across devices.
*   **Accessibility (a11y):** Design with accessibility standards in mind.
*   **Error Handling:** Implement global and component-level error handling for API request failures or unexpected issues.
*   **Loading States:** Provide clear visual feedback (spinners, skeletons) during data fetching or processing.
*   **Internationalization (i18n) & Localization (l10n):** While `preferred_language` is a user attribute, plan for i18n in the frontend if multi-language support is a future goal.
*   **Theming/Styling:** Establish a consistent design system or utilize a UI component library.

This framework provides a detailed starting point. Frontend developers will need to make specific technology choices (React, Vue, Angular, etc.) and further refine these components and user flows during the development process.
