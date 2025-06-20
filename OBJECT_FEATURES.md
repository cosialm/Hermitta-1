# Object Feature Breakdown

This document details the features, attributes, processes, and interactions associated with key data objects in the Kenyan Rental Management System.

---
## I. `User` Object - Feature & Functionality Deep Dive
(Details as previously defined)
### I. User Account Creation & Onboarding
(Details as previously defined)
### II. User Profile Management
(Details as previously defined)
### III. Authentication Management
(Details as previously defined)
### IV. Authorization & Permissions (Features impacting User object directly)
(Details as previously defined)
### V. User Preferences & Settings
(Details as previously defined)
### VI. Linkages to Other Objects
(Details as previously defined)
### VII. Deletion/Deactivation
(Details as previously defined)

---
## II. `Property` Object - Feature & Functionality Deep Dive
(Details as previously defined)
### I. Property Creation & Setup
(Details as previously defined)
### II. Property Information Management & Viewing
(Details as previously defined)
### III. Vacancy Management & Public Listing (Phase 4+)
(Details as previously defined)
### IV. Linkages & Relationships
(Details as previously defined)
### V. Property Deactivation/Archival
(Details as previously defined)

---
## III. `Lease` Object - Feature & Functionality Deep Dive
(Details as previously defined)
### I. Lease Creation & Initiation
(Details as previously defined)
### II. Lease Document & Signature Management
(Details as previously defined)
### III. Active Lease Management
(Details as previously defined)
### IV. Lease Lifecycle Changes (Renewal, Termination)
(Details as previously defined)
### V. Linkages & Relationships
(Details as previously defined)

---
## IV. `Payment` & `FinancialTransaction` Objects (and related) - Feature & Functionality Deep Dive
(Details as previously defined)
### I. `Payment` Object Features & Functionalities (Phase 1 Refined, Phase 2 Enhanced)
(Details as previously defined)
### II. `MpesaPaymentLog` Object Features & Functionalities (Phase 2+)
(Details as previously defined)
### III. `FinancialTransaction` Object Features & Functionalities (Phase 4+)
(Details as previously defined)
### IV. `UserFinancialCategory` Object Features & Functionalities (Phase 4+)
(Details as previously defined)
### V. Linkages & Relationships (Financial Objects)
(Details as previously defined)

---
## V. `MaintenanceRequest` Object & Related - Feature & Functionality Deep Dive
(Details as previously defined)
### I. `MaintenanceRequest` Object Features & Functionalities
(Details as previously defined)
### II. `MaintenanceAttachment` Object Features & Functionalities (Phase 3+)
(Details as previously defined)
### III. `MaintenanceCommunication` Object Features & Functionalities (Phase 3+)
(Details as previously defined)
### IV. `Quote` Object Features & Functionalities (Vendor Portal - Phase 6)
(Details as previously defined)
### V. `VendorInvoice` Object Features & Functionalities (Vendor Portal - Phase 6)
(Details as previously defined)
### VI. Linkages & Relationships (Maintenance Module)
(Details as previously defined)

---
## VI. `RentalApplication` Object & Related - Feature & Functionality Deep Dive
(Details as previously defined)
### I. `LandlordApplicationConfig` Object Features & Functionalities (Phase 3+)
(Details as previously defined)
### II. `RentalApplication` Object Features & Functionalities (Phase 3+)
(Details as previously defined)
### III. `ApplicationDocument` Object Features & Functionalities (Phase 3+)
(Details as previously defined)
### IV. `ApplicationScreening` Object Features & Functionalities (Phase 3+)
(Details as previously defined)
### V. Linkages & Relationships (Rental Application Module)
(Details as previously defined)

---
## VII. `Document` Object & Related - Feature & Functionality Deep Dive
(Details as previously defined)
### I. `Document` Object Features & Functionalities (Phase 4+)
(Details as previously defined)
### II. `DocumentFolder` Object Features & Functionalities (Phase 4+)
(Details as previously defined)
### III. `DocumentShare` Object Features & Functionalities (Phase 4+)
(Details as previously defined)
### IV. Linkages & Relationships (Document Module)
(Details as previously defined)

---
## VIII. `Notification` Object & Related - Feature & Functionality Deep Dive

This section details features related to system notifications, including templates for standardization, landlord-defined rules for automated reminders, and the individual notification records sent to users. (Primarily Phase 2 features, with ongoing relevance).

### I. `NotificationTemplate` Object Features & Functionalities (Primarily Admin Managed - Phase 2+)

This object allows administrators to define standardized templates for various types of notifications sent by the system.

**1.1. Admin Manages Notification Templates**
    *   **Purpose:** To create, view, update, and manage system-wide templates for emails, SMS, and in-app notifications. This ensures consistency in messaging and allows for easy updates to wording or branding.
    *   **NotificationTemplate Attributes Involved:** `template_id` (generated), `name` (e.g., "Rent Reminder - 7 Days Before (SMS)"), `template_type` (Enum, e.g., `RENT_REMINDER`, `PAYMENT_CONFIRMATION`), `delivery_method` (Enum: `EMAIL`, `SMS`, `IN_APP`), `subject_template_en`/`_sw` (for emails), `body_template_en`/`_sw` (with placeholders like `{{tenant_name}}`), `required_placeholders` (list), `is_system_template` (True), `is_active`.
    *   **Process:**
        1.  Admin uses a dedicated interface to manage these templates.
        2.  Defines content for both English and Swahili.
        3.  Specifies placeholders that the system will use to inject dynamic data (e.g., `{{rent_amount}}`, `{{due_date}}`).
    *   **Interactions:**
        *   **LandlordReminderRule Object:** Landlords will select from active, relevant templates when creating their reminder rules.
        *   **Notification Dispatcher (System Process):** The dispatcher uses these templates to generate the final content of a `Notification`.
        *   **AuditLog:** `NOTIFICATION_TEMPLATE_CREATED`, `_UPDATED`, `_DELETED` by Admin.

**1.2. System Uses Templates for Event-Driven Notifications**
    *   **Purpose:** To ensure consistent messaging for automated system-generated notifications (e.g., payment confirmation, new message alert).
    *   **Process:** When a system event occurs (e.g., successful M-Pesa payment), the system identifies the appropriate `NotificationTemplate` based on `template_type` and `delivery_method`, populates it, and creates a `Notification` record for dispatch.

### II. `LandlordReminderRule` Object Features & Functionalities (Landlord Managed - Phase 2+)

This object allows landlords to define their own rules for sending automated reminders to tenants.

**2.1. Landlord Creates/Manages Reminder Rules**
    *   **Purpose:** To enable landlords to set up automated reminders for their tenants regarding events like upcoming rent payments or lease expiries.
    *   **LandlordReminderRule Attributes Involved:** `rule_id` (generated), `landlord_id` (from context), `template_id` (FK to `NotificationTemplate`), `name` (landlord's name for the rule), `days_offset` (e.g., -7 for 7 days before), `offset_relative_to` (Enum: `RENT_DUE_DATE`, `LEASE_END_DATE`), `send_time_hour`, `send_time_minute`, `is_active`.
    *   **Process:**
        1.  Landlord navigates to their notification settings.
        2.  Creates a new rule, selecting an appropriate system `NotificationTemplate` (e.g., "Rent Reminder SMS").
        3.  Defines the trigger logic (e.g., 5 days before `RENT_DUE_DATE`, send at 10:00 AM).
        4.  Activates the rule.
    *   **Interactions:**
        *   **User Object (Landlord):** Links `landlord_id`.
        *   **NotificationTemplate Object:** Links `template_id`.
        *   **Notification Scheduler (System Process):** This scheduler reads active rules to generate `Notification` instances.
        *   **AuditLog:** `LANDLORD_REMINDER_RULE_CREATED`, `_UPDATED`, `_DELETED`.

**2.2. View/List Reminder Rules**
    *   **Purpose:** Landlord can see all the reminder rules they have configured.
    *   **Display:** List of rules with name, template used, trigger logic, active status.

### III. `Notification` Object Features & Functionalities (System Generated & User Interaction)

This object represents an individual notification instance sent or scheduled to be sent to a user.

**3.1. System Generates Notification Record**
    *   **Purpose:** To create a persistent record of a notification to be sent or that has been sent.
    *   **Notification Attributes Set:** `notification_id` (generated), `user_id` (recipient), `type` (from template or event), `delivery_method`, `template_id` (if used), `template_context` (JSON data for placeholders), `status` (initially `SCHEDULED` or `PENDING_SEND`), `scheduled_send_time` (if applicable), `lease_id` (Optional), `reminder_rule_id` (Optional), `related_entity_type`, `related_entity_id`.
    *   **Process:**
        *   **Scheduler-driven:** The Notification Scheduler creates these based on `LandlordReminderRule`s.
        *   **Event-driven:** Other system events (e.g., payment confirmation, new message, document shared) trigger the creation of these records.
    *   **Interactions:**
        *   **User Object:** Links `user_id` (recipient). `User.preferred_language` is used by dispatcher.
        *   **NotificationTemplate, LandlordReminderRule, Lease, Payment etc.:** Contextual links.
        *   **AuditLog:** `NOTIFICATION_CREATED` (system action, might be too verbose to log every instance; perhaps log rule triggers or bulk generations).

**3.2. System Dispatches Notification (via Dispatcher)**
    *   **Purpose:** To process and send the notification content to the user via the specified channel.
    *   **Notification Attributes Updated:** `content` (final message after populating template with `template_context` and user's language), `sent_at`, `status` (updated to `SENT_SUCCESS` or `SENT_FAIL`), `error_message` (if failed).
    *   **Process:**
        1.  Dispatcher picks up `SCHEDULED` (if `scheduled_send_time` is due) or `PENDING_SEND` notifications.
        2.  Retrieves `NotificationTemplate` if `template_id` is present.
        3.  Uses `User.preferred_language` to select EN/SW template versions.
        4.  Populates template with `template_context` to generate final `content`.
        5.  Sends via Email/SMS gateway or stores for In-App retrieval.
        6.  Updates the `Notification` record.
    *   **Interactions:**
        *   **External Gateways (SMS/Email):** API calls to providers like Africa's Talking, SendGrid.
        *   **User Object:** Reads `preferred_language`.
        *   **AuditLog (Potentially):** `NOTIFICATION_SENT_SUCCESS`, `NOTIFICATION_SENT_FAIL`.

**3.3. User Views Notifications (In-App)**
    *   **Purpose:** Allows users to see a list of notifications they have received within the platform.
    *   **Display:** List of `Notification` records where `delivery_method` is `IN_APP` and `user_id` matches current user. Shows `content`, `sent_at`, `read_at`, `type`.
    *   **Process:** User accesses notification center in UI. API fetches their notifications.
    *   **Interactions:** `Notification` records are read.

**3.4. User Marks Notification as Read/Dismissed (In-App)**
    *   **Purpose:** Allows users to manage their in-app notification list.
    *   **Notification Attributes Updated:** `read_at` (timestamped), `status` (updated to `READ`).
    *   **Process:** User interacts with notification in UI (clicks, dismisses).
    *   **Interactions:** **AuditLog** (`NOTIFICATION_MARKED_READ` - can be noisy, consider if needed for every read).

**3.5. System Tracks Delivery Status (from Gateways - Advanced)**
    *   **Purpose:** To update the `Notification` record with actual delivery confirmation from SMS/Email gateways.
    *   **Notification Attributes Updated:** `status` (to `DELIVERY_CONFIRMED` or `DELIVERY_FAILED`), `delivered_at`, `error_message`.
    *   **Process:** Gateways send webhook callbacks to a dedicated system endpoint. System parses callback, finds corresponding `Notification` (e.g., by a gateway message ID stored during dispatch), and updates status.
    *   **Interactions:** **External Gateways**.

### IV. Linkages & Relationships (Notification Module)

*   **`Notification` to `User` (Recipient):** Many-to-One (`user_id`).
*   **`Notification` to `NotificationTemplate`:** Many-to-One (Optional, `template_id`).
*   **`Notification` to `LandlordReminderRule`:** Many-to-One (Optional, `reminder_rule_id`).
*   **`Notification` to `Lease`:** Many-to-One (Optional, `lease_id`).
*   **`Notification` to various `related_entity_type`/`_id` objects.**

*   **`LandlordReminderRule` to `User` (Landlord):** Many-to-One (`landlord_id`).
*   **`LandlordReminderRule` to `NotificationTemplate`:** Many-to-One (`template_id`).

*   **`NotificationTemplate` to `User` (Admin):** (Conceptual) Managed by Admins.

*   **AuditLog:** Creation/updates to `NotificationTemplate` and `LandlordReminderRule` are logged. Generation/sending of critical notifications might be logged.
*   **User Object:** `User.preferred_language` is key for selecting template language.
