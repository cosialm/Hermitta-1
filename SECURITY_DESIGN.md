# Security Design Document - Kenyan Rental Management System

## 1. Introduction

The purpose of this document is to outline the security architecture, policies, and best practices that will be implemented and maintained for the Kenyan Rental Management System. This document serves as a reference for developers, operations personnel, and security reviewers to understand the system's security posture, identify potential threats, and define mitigation strategies. It will be updated iteratively as the system evolves and new threats emerge.

## 2. Threat Model Summary

This section summarizes the key findings from our threat modeling and risk assessment exercises.

### 2.1. Key Assets

The following are identified as critical assets requiring protection:

*   **User Personally Identifiable Information (PII):** Includes names, email addresses, phone numbers, KRA PINs, National ID numbers, physical addresses, financial details (bank/M-Pesa info if stored), and any other data that can identify an individual user (Landlords, Tenants, Staff, Vendors).
*   **Financial Data:** Includes rent payment records, M-Pesa transaction logs, landlord financial configurations (e.g., M-Pesa API keys), expense/income transaction details, and financial reports.
*   **Property Data:** Detailed information about properties, including addresses, ownership details (linked to landlord PII), rental rates, occupancy status, and
    potentially sensitive images or documents.
*   **System Configuration & Credentials:** Includes API keys for third-party services (M-Pesa, SMS/email gateways, cloud services), database credentials, admin panel credentials, and other operational secrets.
*   **System Availability & Integrity:** Ensuring the platform is operational and reliable for users, and that its data and functionalities are accurate and not subject to unauthorized modification.

### 2.2. Potential Threat Actors

The following threat actors have been identified:

*   **Malicious Outsider/Hacker:** External individuals or groups attempting unauthorized access for financial gain, data theft, disruption, or notoriety. Motivations include exploiting vulnerabilities for PII or financial data, deploying ransomware, or causing service outages.
*   **Malicious Tenant:** A registered tenant user attempting to exploit system flaws for personal gain, such as accessing other tenants' data, manipulating their lease/payment records, or causing nuisance to landlords/platform.
*   **Malicious Landlord:** A registered landlord user attempting to exploit system flaws, such as accessing other landlords' data, manipulating financial records, or misusing tenant PII.
*   **Disgruntled Ex-Employee/Insider:** Individuals with previous or current legitimate access who misuse their privileges for data theft, sabotage, or financial fraud. This includes platform administrators, support staff, or even landlord's staff if they have system accounts.
*   **Competitors:** Entities attempting to gain illicit access to business intelligence, user data, or disrupt the platform's operations for competitive advantage.
*   **Automated Bots:** Scripts or automated tools scanning for common vulnerabilities, attempting credential stuffing, spamming forms (e.g., inquiries, applications), or launching DoS attacks.

### 2.3. Key Threats Overview (STRIDE)

Based on the STRIDE methodology, the following key threats have been identified:

*   **Spoofing:**
    *   *User Impersonation:* Unauthorized users gaining access by guessing/stealing credentials (passwords, OTPs, session tokens).
    *   *M-Pesa Callback Spoofing:* Attacker sending fake M-Pesa callback data to fraudulently confirm payments.
    *   *Phishing/Social Engineering:* Tricking users into revealing credentials or sensitive information.
*   **Tampering:**
    *   *Data Modification:* Unauthorized alteration of user PII, financial transaction amounts/statuses, lease agreement terms, or property details.
    *   *M-Pesa Transaction Tampering:* Intercepting and modifying M-Pesa API requests/responses if not properly secured (e.g., amount, account numbers).
    *   *Data In Transit Modification:* Alteration of data exchanged between client and server, or server and third-party services, if not protected by TLS/HTTPS.
*   **Repudiation:**
    *   *Denial of Actions:* Users (tenants, landlords, admins) denying they performed an action (e.g., submitting a maintenance request, approving a quote, changing a setting) if audit logs are insufficient.
    *   *Payment Repudiation:* Tenant falsely claiming a payment was made, or landlord falsely claiming a payment wasn't received (mitigated by M-Pesa logs and system records).
*   **Information Disclosure:**
    *   *M-Pesa API Key/Credential Leakage:* Accidental exposure of M-Pesa API keys, consumer secrets, or passkeys from code, configuration, or logs.
    *   *Bulk PII Exposure:* Unauthorized access to and exfiltration of large sets of user PII (e.g., via database breach, insecure API endpoint).
    *   *Financial Data Breach:* Unauthorized access to sensitive financial transaction history or reports.
    *   *Insecure Direct Object References (IDORs):* Users accessing data belonging to other users by manipulating object IDs in URLs/API calls.
    *   *Common Web Vulnerabilities:* Exposure through XSS, SQL Injection, insecure file uploads, directory traversal, misconfigured S3 buckets, etc.
    *   *Sensitive Data in Logs/URLs:* Accidental logging of passwords, API keys, or PII in URLs.
*   **Denial of Service (DoS):**
    *   *Application-Layer DoS:* Overwhelming specific functionalities (e.g., OTP generation, report generation, property search) with excessive requests.
    *   *Network-Layer DoS/DDoS:* Overwhelming server resources with high-volume traffic.
    *   *Resource Abuse:* Malicious users consuming excessive storage (e.g., large file uploads) or computation (e.g., complex queries).
    *   *Data Deletion/Corruption:* Malicious or accidental deletion/corruption of critical data, rendering the system unusable.
*   **Elevation of Privilege (EoP):**
    *   *Horizontal EoP:* Tenant accessing another tenant's data, or landlord accessing another landlord's data.
    *   *Vertical EoP (User to Admin):* Regular user gaining administrative privileges through exploits or misconfigurations.
    *   *Vertical EoP (Landlord/Tenant to Staff/Vendor with higher access):* User roles gaining unintended access levels.
    *   *System-Level Exploits:* Exploiting OS or unpatched software vulnerabilities on servers to gain system-level access.

### 2.4. Prioritized Risks (Initial High-Level List)

Based on potential impact and likelihood, the following risks are initially prioritized for mitigation (this list will be refined with detailed risk assessment):

1.  **Compromise of M-Pesa API Keys & Credentials:** High impact (financial loss, reputational damage).
2.  **Breach of User Personally Identifiable Information (PII):** High impact (legal penalties under DPA 2019, reputational damage, user trust erosion).
3.  **Unauthorized Access to and Tampering with Financial Data:** High impact (fraud, financial loss, incorrect reporting).
4.  **Admin/Privileged Account Elevation of Privilege:** High impact (full system compromise).
5.  **Application-Layer Denial of Service (DoS) & Resource Abuse:** Medium-High impact (service unavailability, operational costs).
6.  **Common Web Application Vulnerabilities (SQLi, XSS, IDOR):** Medium-High impact (data breaches, unauthorized access, defacement).
7.  **Insecure Handling of User Authentication & Session Management:** Medium-High impact (account takeovers).
8.  **Insufficient Audit Trails for Critical Actions:** Medium impact (difficulty in incident response and repudiation disputes).

This summary will inform the subsequent sections of this Security Design Document, which will detail specific security controls, policies, and procedures.

## 3. Secure Software Development Lifecycle (SSDLC) Principles & Guidelines

The following principles and guidelines form the basis of our Secure Software Development Lifecycle (SSDLC) for the Kenyan Rental Management System. These are to be adhered to throughout the design, development, testing, and deployment phases.

### 3.1. Secure by Design

*   **Explanation:** Security must be an integral part of the system design from the outset, not an afterthought. This involves proactively building defenses and making secure choices at every stage.
*   **Key Aspects for this System:**
    *   **Principle of Least Privilege:** Users, services, and system components should only be granted the minimum permissions necessary to perform their intended functions. This applies to database access, API endpoint authorization, and file system permissions.
    *   **Defense in Depth:** Implement multiple layers of security controls so that if one control fails, others can still protect assets. For example, input validation, parameterized queries, authorization checks, and web application firewalls (WAFs).
    *   **Secure Defaults:** Default configurations should be secure. For instance, new user accounts should have strong password policies enforced, and sensitive features should be disabled by default.
    *   **Attack Surface Reduction:** Minimize the number of exposed endpoints, services, and libraries to reduce potential points of entry for attackers. Regularly review and remove unused code or features.

### 3.2. Input Validation (Server-Side Critical)

*   **Explanation:** All input received by the application (from users, APIs, files, etc.) must be rigorously validated on the server-side to prevent malformed data, injection attacks, and other exploits. Client-side validation is for UX but not a security control.
*   **Key Aspects for this System:**
    *   **Type Validation:** Ensure data is of the expected type (e.g., integer, string, boolean, date).
    *   **Length Validation:** Enforce minimum and maximum lengths for strings and numbers.
    *   **Format/Range Validation:** Check if data conforms to specific formats (e.g., email, phone number, KRA PIN, date formats) or falls within an acceptable range (e.g., rent amount > 0).
    *   **Allow-list Validation:** Whenever possible, validate input against a strict list of allowed characters or values (e.g., for enums, specific commands). Deny-lists are generally weaker.
    *   **Business Logic Validation:** Ensure input is valid within the context of the application's business rules (e.g., lease start date before end date, payment amount not exceeding amount due for certain payment types).
    *   **File Upload Validation:**
        *   **Type Checking:** Validate file types based on magic numbers and MIME types, not just extensions. Only allow expected file types (e.g., PDF, JPG, PNG for documents).
        *   **Malware Scanning:** Scan uploaded files for malware before storing or processing.
        *   **Size Limits:** Enforce strict file size limits to prevent resource exhaustion.
        *   **Storage Location:** Store uploaded files in a non-web-accessible location (e.g., S3 bucket with restricted access, dedicated file store outside webroot) and serve them via a controlled endpoint that enforces authorization.
        *   **Safe Filenames:** Generate safe, unique filenames for stored files to prevent directory traversal or overwrite attacks. Do not use user-supplied filenames directly for storage.

### 3.3. Output Encoding (Contextual)

*   **Explanation:** Properly encode all output data before it is rendered in a user's browser or consumed by another system to prevent Cross-Site Scripting (XSS) and other injection attacks. The type of encoding depends on the context where the data is displayed.
*   **Key Aspects for this System:**
    *   **HTML Context:** Use HTML entity encoding for data displayed within HTML body content.
    *   **HTML Attribute Context:** Use HTML attribute encoding for data inserted into HTML attributes.
    *   **JavaScript Context:** Use JavaScript string encoding for data inserted into JavaScript code blocks or event handlers. Avoid inserting user data directly into scripts where possible.
    *   **URL Context:** Use URL encoding for data inserted into URLs (e.g., query parameters).
    *   **CSS Context:** Use CSS encoding if data is inserted into stylesheets (rare, generally avoid).
    *   Utilize templating engines and libraries that offer automatic contextual encoding features.

### 3.4. Parameterized Queries / ORM Usage

*   **Explanation:** To prevent SQL Injection vulnerabilities, always use parameterized queries (prepared statements) or Object-Relational Mappers (ORMs) that inherently use parameterized queries. Never construct SQL queries by directly concatenating user-supplied input.
*   **Key Aspects for this System:**
    *   If using an ORM (e.g., SQLAlchemy, Django ORM, GORM), leverage its built-in mechanisms for data access, which typically handle SQLi prevention.
    *   If writing raw SQL, ensure all user input is passed as parameters to prepared statements, not embedded directly in the query string.

### 3.5. Authentication and Authorization

*   **Explanation:** Implement strong authentication mechanisms to verify the identity of users and services. Enforce robust authorization checks on every request to ensure users and services can only access resources and perform actions they are explicitly permitted to.
*   **Key Aspects for this System:** (Detailed in subsequent Security Controls section)
    *   Strong password policies, secure credential storage (hashing with salt).
    *   Multi-Factor Authentication (MFA) options, especially for admin/landlord roles.
    *   Role-Based Access Control (RBAC) and potentially fine-grained permissions.
    *   Authorization checks applied consistently at the API endpoint and service layers.

### 3.6. Session Management

*   **Explanation:** Securely manage user sessions to prevent session hijacking, fixation, and other session-related attacks.
*   **Key Aspects for this System:** (Detailed in subsequent Security Controls section)
    *   Generate strong, unpredictable session IDs.
    *   Use secure cookie flags (HttpOnly, Secure, SameSite).
    *   Implement session timeouts (idle and absolute).
    *   Provide secure logout functionality that invalidates sessions.

### 3.7. Error Handling & Secure Logging

*   **Explanation:** Implement error handling that does not expose sensitive system information to users. Log errors and security-relevant events comprehensively on the server-side for monitoring, auditing, and incident response.
*   **Key Aspects for this System:**
    *   **User-Facing Errors:** Display generic error messages to users (e.g., "An unexpected error occurred. Please try again later.").
    *   **Server-Side Logs:** Log detailed error information (stack traces, request details excluding sensitive data) on the server for debugging.
    *   **Audit Logging:** Log security-relevant events (e.g., login attempts, password changes, access to sensitive data, critical transactions, admin actions) with timestamps, user IDs, and source IP addresses.
    *   **No Sensitive Data in Logs:** Ensure passwords, API keys, session tokens, full PII, or other sensitive data are NEVER written to logs. Sanitize or mask such data if necessary.

### 3.8. Cryptography

*   **Explanation:** Use strong, industry-standard cryptographic algorithms and libraries for protecting data at rest and in transit. Avoid implementing custom cryptographic algorithms.
*   **Key Aspects for this System:**
    *   **HTTPS/TLS:** Enforce HTTPS for all client-server communication and server-to-server communication where applicable. Use up-to-date TLS configurations.
    *   **Data at Rest Encryption:** Encrypt sensitive data stored in the database (e.g., M-Pesa API keys, certain PII fields) using vetted encryption libraries and proper key management.
    *   **Password Hashing:** Use strong, adaptive hashing algorithms with unique salts for storing user passwords (e.g., Argon2, bcrypt, scrypt).
    *   **Key Management:** Securely manage all cryptographic keys (e.g., using a Hardware Security Module (HSM), cloud provider's Key Management Service (KMS), or other secure key vault solutions).

### 3.9. Dependency Management

*   **Explanation:** Regularly review, update, and manage third-party libraries and dependencies used in the application and infrastructure. Outdated or vulnerable dependencies are a common attack vector.
*   **Key Aspects for this System:**
    *   **Inventory:** Maintain an inventory of all third-party components and their versions.
    *   **Vulnerability Scanning:** Use tools (e.g., Dependabot, Snyk, OWASP Dependency-Check) to automatically scan dependencies for known vulnerabilities.
    *   **Timely Updates:** Establish a process for promptly updating vulnerable dependencies, testing them in a staging environment before production deployment.
    *   **Remove Unused Dependencies:** Regularly remove any dependencies that are no longer needed to reduce the attack surface.

### 3.10. Security in Code Reviews

*   **Explanation:** Integrate security considerations into the standard code review process. Every code change should be reviewed for potential security flaws before being merged into the main codebase.
*   **Key Aspects for this System:**
    *   **Security Checklist:** Develop a security checklist for code reviewers (e.g., checking for common vulnerabilities like OWASP Top 10, adherence to SSDLC principles like input validation, output encoding, proper authorization).
    *   **Peer Review:** At least one other developer should review code for security implications.
    *   **Tooling:** Use static analysis (SAST) tools to identify potential issues early in the development cycle and during reviews.

### 3.11. Security Testing

*   **Explanation:** Conduct various forms of security testing throughout the SSDLC and post-deployment to identify and remediate vulnerabilities.
*   **Key Aspects for this System:** (Detailed in a subsequent Security Testing Strategy section)
    *   **Static Application Security Testing (SAST):** Analyzing source code for vulnerabilities without executing it.
    *   **Dynamic Application Security Testing (DAST):** Testing the running application for vulnerabilities from the outside.
    *   **Penetration Testing:** Authorized simulated attacks on the system to identify exploitable vulnerabilities.
    *   **Vulnerability Assessments:** Regular scans and assessments to identify known vulnerabilities.
    *   Security testing should cover all components: web application, APIs, mobile apps (if any), infrastructure.

## 4. Authentication Design

This section details the authentication mechanisms for the Kenyan Rental Management System, ensuring robust user identity verification.

### 4.1. Password Policies

Strong password policies will be enforced to protect user accounts from brute-force and dictionary attacks.
*   **Minimum Length:** Passwords must be at least 10 characters long (preferably 12+).
*   **Complexity:** Passwords must include a mix of uppercase letters, lowercase letters, numbers, and special characters (e.g., !@#$%^&*).
*   **Password History:** The system will prevent users from reusing a configurable number of their previous passwords (e.g., last 5 passwords).
*   **Account Lockout:** Accounts will be temporarily locked after a configurable number of failed login attempts (e.g., 5 attempts) from a specific IP address or for a specific account. Lockout duration will increase with repeated failures.
*   **Secure Password Reset:**
    *   Password reset mechanisms (email or SMS OTP) will use secure, time-limited, single-use tokens/OTPs.
    *   Users will be required to verify their identity (via email link or OTP) before being allowed to set a new password.
    *   Notifications will be sent to the user upon password change.
*   **Password Hashing:** Passwords will be stored using a strong, adaptive, salted hashing algorithm (e.g., Argon2id or bcrypt). Plaintext passwords will never be stored.

### 4.2. Multi-Factor Authentication (MFA)

MFA provides an additional layer of security beyond username and password.
*   **Primary Method (TOTP):** Time-based One-Time Passwords (TOTP) using authenticator apps (e.g., Google Authenticator, Authy) will be the primary MFA method.
    *   **User Model Changes:** The `User` model includes `mfa_secret_key_encrypted` (for storing the encrypted TOTP secret), `is_mfa_enabled` (boolean), and `mfa_recovery_codes_hashed` (JSON array of hashed one-time recovery codes).
    *   **Setup Workflow:**
        1.  User initiates MFA setup.
        2.  System generates a unique secret key for the user.
        3.  Secret key is presented to the user as a QR code and in text format.
        4.  User scans QR code/enters key into their authenticator app.
        5.  User verifies by entering a TOTP generated by their app.
        6.  Upon successful verification, `is_mfa_enabled` is set to true, and the (encrypted) `mfa_secret_key_encrypted` is stored.
        7.  A set of one-time recovery codes is generated, hashed, and presented to the user to store securely. These codes can be used if the authenticator device is lost.
    *   **Login Workflow:** If MFA is enabled, after successful password validation, the user is prompted to enter a TOTP from their authenticator app.
*   **Secondary Method (SMS OTP - Optional):** SMS-based OTP can be offered as an alternative MFA method, though it's considered less secure than TOTP due to risks like SIM swapping. If implemented, it will use the user's verified phone number.
*   **MFA for Privileged Roles:** MFA will be strongly recommended, and potentially mandated, for users with privileged roles (e.g., Admin, Landlord, Staff with financial access).

### 4.3. Session Management

Secure session management is crucial to protect authenticated user sessions from hijacking or unauthorized access.
*   **Session Token Generation:** Session tokens/IDs will be generated using a cryptographically secure pseudo-random number generator (CSPRNG) and will have sufficient length and entropy to prevent guessing.
*   **Session Storage:** Prefer server-side session storage (e.g., in a secure database or Redis cache) with only a session ID token passed to the client. Avoid storing excessive sensitive data in client-side storage (e.g., JWTs with PII, unless strictly necessary and payload is encrypted).
*   **Session Timeouts:**
    *   **Idle Timeout:** Sessions will automatically expire after a period of inactivity (e.g., 15-30 minutes).
    *   **Absolute Timeout:** Sessions will have a maximum lifetime (e.g., 8-24 hours), after which re-authentication is required, regardless of activity.
*   **Secure Cookie Flags (If using cookies for session tokens):**
    *   `HttpOnly`: Prevents client-side JavaScript from accessing the session cookie, mitigating XSS.
    *   `Secure`: Ensures the session cookie is only transmitted over HTTPS.
    *   `SameSite` (Lax or Strict): Provides protection against Cross-Site Request Forgery (CSRF).
*   **Secure Logout:** Logout functionality will securely invalidate the session on both the client and server-side. Simply deleting the client-side token is insufficient.
*   **Session Regeneration:** Session IDs should be regenerated after any privilege level change (e.g., login, password change, MFA setup).

## 5. Authorization Design

Authorization determines what actions an authenticated user is permitted to perform and what data they are allowed to access.

### 5.1. Role-Based Access Control (RBAC)

The system will implement RBAC based on defined user roles.
*   **Defined Roles (from `User` model):** `LANDLORD`, `TENANT`, `STAFF`, `VENDOR`, `ACCOUNTANT`, `ADMIN`.
*   **Permission Mapping:** Each role will have a set of associated permissions. These permissions define access to specific API endpoints, system functionalities, and data types. Detailed permission mapping (e.g., which role can access which API endpoint with which HTTP method) will be maintained and enforced at the API gateway or application layer. For `STAFF` roles, more granular JSON-based permissions (`staff_permissions` in `User` model) might further refine access.

### 5.2. Object-Level Permissions (Ownership & Contextual Access)

Beyond role-based permissions, the system must enforce object-level permissions, ensuring users can only access and manipulate data they own or have a legitimate contextual relationship with.
*   **Examples:**
    *   A `LANDLORD` can only manage properties, leases, and financial transactions they own.
    *   A `TENANT` can only view their own lease details, payment history, and submit maintenance requests for their leased property.
    *   A `VENDOR` can only access maintenance requests specifically assigned to them.
    *   A `STAFF` member might only have access to properties, leases, or tenants they are explicitly assigned to manage (via `User.staff_permissions` or similar mechanism).
*   **Implementation:** These checks must be performed on every relevant data access request by verifying the authenticated user's ID against ownership fields (e.g., `landlord_id`, `tenant_id`) or association tables related to the requested data object.

### 5.3. Consistent Server-Side Enforcement

All authorization checks, both role-based and object-level, **must** be performed on the server-side within API endpoints and business logic. Client-side UI elements may hide or show functionality based on user role, but this is for UX only and not a security measure. The server must never trust that the client has correctly enforced permissions.

### 5.4. Privilege Escalation Prevention

Mechanisms will be in place to prevent privilege escalation.
*   **Regular Review:** Periodically review role definitions and permission assignments to ensure they adhere to the principle of least privilege.
*   **Input Validation:** Strict input validation for any parameters that might influence authorization decisions.
*   **Secure API Design:** Avoid API designs that might inadvertently expose ways to bypass authorization checks (e.g., by manipulating user IDs or roles in requests if not properly validated against the authenticated session).

## 6. Data Security & Privacy Enhancements

This section outlines specific measures to protect data at rest and in transit, manage secrets securely, and adhere to data privacy principles relevant to the Kenyan context, including the Data Protection Act, 2019.

### 6.1. Data Encryption

Encryption is a fundamental control for protecting data confidentiality and integrity.

#### 6.1.1. Encryption in Transit

*   **Explanation:** All data exchanged between the client (user's browser, mobile app) and the server, as well as between internal system components (e.g., server to database, server to M-Pesa API), must be encrypted.
*   **Key Considerations:**
    *   **HTTPS/TLS:** Mandate HTTPS (HTTP Secure) using Transport Layer Security (TLS 1.2 or higher) for all external and internal web communications. Redirect all HTTP requests to HTTPS.
    *   **Strong Cipher Suites:** Configure web servers and other TLS endpoints to use strong, industry-standard cipher suites and disable weak/deprecated ones.
    *   **HTTP Strict Transport Security (HSTS):** Implement the HSTS header to instruct browsers to only communicate with the application over HTTPS, preventing downgrade attacks.
    *   **Secure API Communication:** Ensure all API endpoints, including those for M-Pesa integration and other third-party services, use HTTPS.

#### 6.1.2. Encryption at Rest

*   **Explanation:** Data stored persistently in databases, file storage, or backups must be encrypted to protect against unauthorized access if the underlying storage is compromised.
*   **Key Considerations:**
    *   **Database-Level Encryption:**
        *   **Transparent Data Encryption (TDE):** Where available (e.g., in managed cloud databases like AWS RDS, Azure SQL Database), enable TDE to encrypt the entire database at rest, including data files, log files, and backups. This provides a baseline level of protection.
    *   **Application-Level Encryption (ALE):** For highly sensitive specific fields, implement ALE before writing to the database.
        *   **Target Fields:** `LandlordMpesaConfiguration` (consumer_key, consumer_secret, passkey), `User.mfa_secret_key_encrypted`, potentially certain PII fields if deemed necessary by risk assessment.
        *   **Algorithm:** Use a strong, authenticated symmetric encryption algorithm like AES-256 in GCM or CBC mode.
        *   **Key Management:** The master encryption key used for ALE must be managed securely via a dedicated secrets manager (see section 6.2). This key should NOT be stored in code or configuration files.
        *   **Key Rotation:** Establish a strategy for rotating the master encryption key and re-encrypting data periodically or when a key compromise is suspected.
    *   **File Storage Encryption:** Ensure files uploaded to cloud storage (e.g., S3, Azure Blob Storage) are encrypted at rest using server-side encryption (SSE) options provided by the cloud provider.

### 6.2. Secrets Management

*   **Explanation:** Securely manage all secrets, including API keys, database credentials, encryption keys, and session secrets, to prevent unauthorized access and use.
*   **Key Considerations:**
    *   **Dedicated Secrets Manager:** Mandate the use of a dedicated secrets management solution (e.g., HashiCorp Vault, AWS Secrets Manager, Google Cloud Secret Manager, Azure Key Vault). Do not store secrets in code, configuration files, or environment variables in version control.
    *   **Types of Secrets to Manage:**
        *   Database credentials.
        *   API keys for third-party services (M-Pesa, SMS/email gateways, payment processors).
        *   Application-level encryption master key(s).
        *   Session signing/encryption secrets.
        *   Credentials for accessing other internal services.
    *   **Access Control:** Implement strict access controls within the secrets manager, adhering to the principle of least privilege. Only authorized applications/services should have access to specific secrets they need.
    *   **Auditing:** Ensure the secrets manager provides detailed audit logs of when secrets are accessed, by whom/what, and any changes made.
    *   **Rotation:** Implement regular rotation of secrets, especially database credentials and API keys, where supported by the service.

### 6.3. Data Minimization & Pseudonymization

*   **Explanation:** Collect and retain only the data that is strictly necessary for the intended purpose, in line with the Data Protection Act, 2019 (DPA 2019) principles. Pseudonymization can be used to reduce risks when using data in non-production environments.
*   **Key Considerations:**
    *   **Purpose Limitation:** For each piece of data collected, clearly define and document the purpose. Avoid collecting data "just in case" it might be useful later.
    *   **Regular Review:** Periodically review data models and collection processes to identify and remove any data fields that are no longer necessary.
    *   **Pseudonymization for Non-Production:** For development, testing, and analytics environments, use pseudonymized or anonymized data where possible to reduce the risk associated with using real PII. This involves replacing direct identifiers with pseudonyms or masking data.
    *   **User Interface Design:** Design forms and user interfaces to only request mandatory information, clearly distinguishing it from optional fields.

### 6.4. Secure Logging & Monitoring

*   **Explanation:** Implement comprehensive logging for security events and system activity, but ensure logs themselves do not become a source of sensitive information disclosure. Monitor logs for suspicious activity.
*   **Key Considerations:**
    *   **CRITICAL: No Sensitive Data in Logs:** Strictly prohibit the logging of sensitive data such as passwords, full credit card numbers (if ever handled, though likely outsourced), M-Pesa PINs, API keys, session tokens, MFA secrets, or excessive PII that is not essential for the log's purpose. Implement sanitization routines if necessary.
    *   **Security-Relevant Events:** Log key security events, including but not limited to:
        *   Authentication successes and failures (including source IP, user agent).
        *   Authorization failures.
        *   Password reset attempts and changes.
        *   MFA status changes and verification attempts.
        *   Access to sensitive functions or data (e.g., viewing M-Pesa configurations, exporting user data).
        *   Changes to user roles or permissions.
        *   Significant data modification events (e.g., lease termination, large payment recordings).
        *   Admin user activities.
    *   **Log Integrity & Protection:** Protect logs from unauthorized access, modification, or deletion. Use centralized logging solutions that provide secure storage and access controls. Consider log signing or write-once storage if high integrity is required.
    *   **Monitoring & Alerts:** Implement real-time or near real-time monitoring of logs for suspicious patterns, repeated failures, or known indicators of compromise. Configure alerts for critical security events to enable prompt investigation.

### 6.5. Data Retention & Disposal

*   **Explanation:** Establish and enforce clear policies for how long different types of data are retained and how they are securely disposed of once they are no longer needed for legal, regulatory, or legitimate business purposes. This is a key requirement of the DPA 2019.
*   **Key Considerations:**
    *   **Data Retention Schedule:** Define specific retention periods for different data categories (e.g., user accounts, lease agreements, financial transactions, application data, logs). Base these periods on Kenyan legal requirements (e.g., financial record keeping) and business needs.
    *   **Secure Deletion:** Implement mechanisms for securely deleting data from active systems and backups once its retention period has expired or upon a valid erasure request from a user (as per DPA 2019 rights). This means more than just marking a record as "deleted"; it should be irrecoverable.
    *   **Anonymization/Pseudonymization for Archival:** For data that needs to be kept longer for statistical or analytical purposes but where PII is not required, consider anonymization or pseudonymization techniques.
    *   **User-Requested Deletion:** Implement processes to handle data subject rights for erasure under the DPA 2019, ensuring all relevant data is securely deleted in accordance with the law.
    *   **Backup Data:** Ensure retention policies also apply to data backups, and that expired data is eventually removed from backups as well.

## 7. API Security Hardening

APIs are critical interfaces to the system's data and functionality, and thus require specific security measures to protect against common and emerging threats.

### 7.1. Strong Authentication & Authorization (API Context)

*   **Explanation:** Every API endpoint (except those explicitly designed as public, e.g., for property vacancy listings) must enforce strong authentication to verify the identity of the requesting client/user. Subsequently, robust authorization checks must be applied to ensure the authenticated entity has the necessary permissions for the requested resource and action.
*   **Key Considerations:**
    *   **Authentication:** Utilize secure token-based authentication (e.g., OAuth 2.0, JWTs with secure signing algorithms like RS256/ES256). Tokens should be short-lived with a clear refresh mechanism. API keys for server-to-server communication must be managed securely.
    *   **Authorization:** Reiterate the enforcement of Role-Based Access Control (RBAC) and Object-Level Permissions on every API call. No assumptions should be made based on client-side checks.

### 7.2. Robust Input Validation (Server-Side)

*   **Explanation:** All data received by API endpoints must be rigorously validated on the server-side. This includes URL parameters, query parameters, request bodies (e.g., JSON, XML), and HTTP headers. Invalid input is a primary vector for many API attacks.
*   **Key Considerations:**
    *   **Schema Validation:** Use schema validation libraries (e.g., JSON Schema) to validate the structure, data types, formats, and ranges of incoming request bodies.
    *   **Parameter Validation:** Validate all individual parameters for type, length, format, and allowed values.
    *   **Error Handling:** Reject requests with invalid data immediately with a `400 Bad Request` status code and clear (but not overly revealing) error messages.
    *   **Contextual Validation:** Pay special attention to data that will be used in database queries (prevent NoSQL injection if applicable), file system paths (prevent directory traversal), or calls to external systems.

### 7.3. Output Encoding & Content Types

*   **Explanation:** Ensure API responses use appropriate `Content-Type` headers (e.g., `application/json`) and that data is correctly encoded to prevent XSS if the API response might be rendered directly in a browser context by older or misconfigured clients.
*   **Key Considerations:**
    *   **Consistent `Content-Type`:** Set `Content-Type: application/json; charset=utf-8` for JSON responses.
    *   **Avoid HTML in JSON:** Generally, avoid embedding HTML within JSON responses that might be insecurely rendered by clients. If HTML is necessary, ensure it's sanitized or comes from a trusted source.
    *   **Echoing Input:** Be cautious about echoing user-supplied input in API responses without proper validation and encoding, as this can lead to XSS.

### 7.4. Rate Limiting & Throttling

*   **Explanation:** Implement rate limiting and throttling on API endpoints to protect against DoS attacks, brute-force attempts (on auth endpoints), and general resource abuse.
*   **Key Considerations:**
    *   **Per User/IP:** Apply rate limits based on authenticated user ID and/or source IP address.
    *   **Sensitive Endpoints:** Apply stricter rate limits to sensitive endpoints like login, OTP generation, password reset, and resource-intensive operations.
    *   **HTTP Status Code:** Return `429 Too Many Requests` when rate limits are exceeded. Include `Retry-After` header if appropriate.
    *   **Tiered Limiting:** Consider different rate limiting tiers for authenticated vs. unauthenticated users, or different user roles/subscription levels.
    *   **Logging & Monitoring:** Log rate limit events to detect abuse patterns.

### 7.5. Protection Against Common API Vulnerabilities (OWASP API Security Top 10 Focus)

*   **Explanation:** Proactively design and test against common API vulnerabilities, such as those highlighted by the OWASP API Security Top 10 project.
*   **Key Considerations (Examples):**
    *   **API1:2023 Broken Object Level Authorization (BOLA):** Enforce strict object-level permissions (see 5.2). Validate user's right to access/modify specific resource instances on every request.
    *   **API2:2023 Broken Authentication:** Implement strong authentication (see 4.0), secure credential handling, and MFA. Protect against credential stuffing and brute-force.
    *   **API3:2023 Broken Object Property Level Authorization:** If allowing partial updates (e.g. PATCH), ensure user is authorized to modify each specific property in the request, not just the object as a whole. Implement schema validation for request bodies to prevent unexpected properties.
    *   **API4:2023 Unrestricted Resource Consumption:** Implement rate limiting, pagination, query complexity limits, and file size limits (see 7.4 and 3.2).
    *   **API5:2023 Broken Function Level Authorization:** Ensure authorization checks are applied not just for data access but also for specific functions/actions a user role can perform.
    *   **API6:2023 Unrestricted Access to Sensitive Business Flows:** Protect business flows like payment initiation, user registration, or password reset from automated abuse using CAPTCHAs, rate limiting, or step-up authentication.
    *   **API7:2023 Server Side Request Forgery (SSRF):** Validate and sanitize any URLs or hostnames received in requests that the server might use to make outgoing requests. Use allow-lists for target domains.
    *   **API8:2023 Security Misconfiguration:** Regularly review configurations of servers, frameworks, cloud services, and security headers. Use automated tools to check for misconfigurations.
    *   **API9:2023 Improper Inventory Management:** Maintain a clear inventory of all API versions and endpoints, including their exposure (public, partner, internal) and deprecate/protect old versions.
    *   **API10:2023 Unsafe Consumption of APIs:** When integrating with third-party APIs (like M-Pesa), validate their SSL certificates, securely handle their API keys, validate input/output, and handle errors gracefully.

### 7.6. Secure API Headers

*   **Explanation:** Utilize HTTP security headers to provide additional defense-in-depth for API clients, particularly web browsers.
*   **Key Considerations (Recommended Headers):**
    *   **`Strict-Transport-Security` (HSTS):** `Strict-Transport-Security: max-age=31536000; includeSubDomains` - Enforces HTTPS.
    *   **`X-Content-Type-Options`:** `X-Content-Type-Options: nosniff` - Prevents browsers from MIME-sniffing a response away from the declared content-type.
    *   **`X-Frame-Options`:** `X-Frame-Options: DENY` (or `SAMEORIGIN`) - Protects against clickjacking if APIs are ever accessed via iframes (less common for pure data APIs but good practice).
    *   **`Content-Security-Policy` (CSP):** (Good Practice, more complex) `Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; frame-ancestors 'none';` - Helps prevent XSS and other injection attacks. For data APIs, a stricter policy like `default-src 'none'; frame-ancestors 'none';` might be applicable if no direct browser rendering is expected.
    *   **`X-XSS-Protection`:** `X-XSS-Protection: 0` - This header is often set to 0 to disable legacy browser XSS filters, as modern browsers rely on CSP which is more effective. If CSP is not fully implemented, `1; mode=block` might be considered but CSP is preferred.

### 7.7. API Versioning

*   **Explanation:** Plan for API versioning from the start to allow for future updates and changes without breaking existing client integrations.
*   **Key Considerations:**
    *   **Strategy:** Common strategies include URL path versioning (e.g., `/api/v1/...`, `/api/v2/...`), header versioning (e.g., `Accept: application/vnd.myapi.v1+json`), or query parameter versioning (e.g., `?version=1`). URL path versioning is often clearest.
    *   **Deprecation Policy:** Clearly communicate deprecation timelines for older API versions.
    *   **Documentation:** Maintain clear documentation for each API version.

### 7.8. Secure File Uploads (API Context)

*   **Explanation:** API endpoints that handle file uploads require specific security measures, reiterating points from section 3.2 but in the direct API context.
*   **Key Considerations:**
    *   **Authentication & Authorization:** Ensure only authenticated and authorized users can upload files.
    *   **Type & Size Validation:** Strictly validate file types (MIME, magic numbers) and enforce size limits on the server-side for each API request.
    *   **Malware Scanning:** Scan files for malware upon upload before they are stored or processed further.
    *   **Secure Storage:** Store uploaded files in a non-web-accessible location with unique, system-generated filenames. Access files via controlled API endpoints that enforce authorization.
    *   **Content-Disposition:** When serving files, use `Content-Disposition: attachment; filename="user_friendly_name.ext"` to encourage browsers to download rather than render, especially for potentially risky types.
    *   **Rate Limiting:** Apply rate limiting to file upload endpoints to prevent abuse.

## 8. M-Pesa Integration Security

Specific security considerations for the integration with Safaricom M-Pesa APIs, particularly for STK Push payments and callback handling. This is critical due to the direct financial implications.

### 8.1. Secure Credential Storage & Handling (M-Pesa)

*   **Explanation:** M-Pesa API credentials (Consumer Key, Consumer Secret, Passkey, Shortcodes) are highly sensitive and must be protected with utmost care.
*   **Key Considerations:**
    *   **Encryption at Rest:** As detailed in section 6.1.2, these credentials stored in the `LandlordMpesaConfiguration` model must be encrypted using strong application-level encryption (e.g., AES-256 GCM).
    *   **Secrets Manager for Master Key:** The master encryption key used for encrypting/decrypting these M-Pesa credentials must be stored in a dedicated secrets manager (see section 6.2).
    *   **Strict Access Control:** Access to the M-Pesa configuration data (even encrypted) within the database and to the secrets manager should be restricted to only essential backend services. Human access should be minimal, audited, and require MFA.
    *   **Just-in-Time Decryption:** Decrypt credentials only in memory when an API call to M-Pesa is about to be made. Do not store decrypted credentials anywhere.
    *   **Audit Trails:** Log all access and modification attempts to `LandlordMpesaConfiguration` records. Audit access to the master encryption key in the secrets manager.
    *   **Secure Configuration Interface:** The API endpoints for landlords to configure their M-Pesa details must be robustly authenticated and authorized.

### 8.2. Secure STK Push Initiation

*   **Explanation:** The process of initiating an STK (SIM Toolkit) push to a tenant's phone for payment must be secure to prevent fraud or misuse.
*   **Key Considerations:**
    *   **Rigorous Input Validation:** Before making an STK push API call:
        *   Validate the `amount` against the expected payment amount for the lease (e.g., from `Payment.expected_amount`).
        *   Validate the `phone_number` format (Kenyan M-Pesa format).
        *   Verify the association between the tenant and the lease for which payment is being initiated.
    *   **Idempotency:** Implement idempotency for STK push requests (e.g., using `MerchantRequestID` from `MpesaPaymentLog`) to prevent accidental duplicate pushes and payments for the same payment intent, especially if client-side retries occur.
    *   **Rate Limiting:** Apply rate limiting per tenant and/or per lease for STK push initiation requests to prevent abuse of the M-Pesa API and potential spamming of users.
    *   **User Consent:** Ensure the tenant has clearly initiated the payment request through the UI before an STK push is sent.

### 8.3. Callback URL Security

*   **Explanation:** The callback URL registered with Safaricom for receiving M-Pesa transaction status updates is a critical entry point and must be secured.
*   **Key Considerations:**
    *   **HTTPS Enforcement:** The callback URL must use HTTPS to protect data in transit.
    *   **Dedicated & Non-Guessable URL:** Use a dedicated, potentially unguessable or randomized URL path for the M-Pesa callback endpoint to reduce exposure to unsolicited traffic.
    *   **Platform vs. Landlord-Specific Callbacks:**
        *   **Platform Default:** A single, platform-wide callback URL is generally easier to secure and manage. The payload from M-Pesa (containing `CheckoutRequestID`) is then used to route the update to the correct transaction log.
        *   **Landlord-Specific:** If `LandlordMpesaConfiguration.callback_url_override` is used, ensure these custom URLs also adhere to HTTPS and are robustly implemented. This approach increases complexity.
    *   **Access Control:** While the endpoint is public (for M-Pesa to call), application logic should only process valid, expected callbacks.

### 8.4. Callback Validation (Authenticity & Integrity)

*   **Explanation:** This is a CRITICAL step to prevent attackers from spoofing M-Pesa payment confirmations. All incoming callback data must be thoroughly validated before updating payment statuses.
*   **Key Considerations:**
    *   **Source IP Whitelisting:** If Safaricom provides a list of fixed IP addresses from which callbacks originate, implement IP whitelisting for the callback endpoint. This is a strong first line of defense.
    *   **Request Signing/Verification (Ideal but check Safaricom support):** If Safaricom signs callback requests (e.g., using a shared secret or public/private key cryptography), verify this signature on every incoming callback. This is the most robust method for ensuring authenticity.
    *   **Cross-Reference IDs:**
        *   Validate that the `CheckoutRequestID` (and/or `MerchantRequestID`) in the callback payload matches an existing record in `MpesaPaymentLog` with an appropriate pending status (e.g., `STK_PUSH_SUCCESSFUL`, `TIMEOUT_AWAITING_CALLBACK`).
    *   **Amount Validation:** Compare the `Amount` in the callback payload with the `amount_requested` in the `MpesaPaymentLog` or associated `Payment` record. Discrepancies should be flagged.
    *   **M-Pesa Receipt Number:** Validate the format of the `MpesaReceiptNumber`. Check for uniqueness (within a reasonable timeframe or against recent transactions) to prevent replay attacks where an old, valid callback is resent.
    *   **Secure and Idempotent Processing:** Design the callback processing logic to be idempotent. If the same valid callback is received multiple times (e.g., due to M-Pesa retries), it should not result in duplicate payment crediting or other side effects. This usually involves checking the current status of the `MpesaPaymentLog` or `Payment` before processing.
    *   **Parameter Validation:** Validate all other expected parameters in the callback payload for type, format, and plausibility.

### 8.5. Transaction Status Query API Security (If Used)

*   **Explanation:** If the system uses M-Pesa's Transaction Status Query API (e.g., after an STK push timeout), calls to this API must also be secured.
*   **Key Considerations:**
    *   **Secure Authentication:** Calls to the M-Pesa Query API will require authentication using the landlord's (or platform's) M-Pesa credentials. Ensure these are handled securely as per section 8.1.
    *   **Authorization for Internal Triggers:** Internal API endpoints or system jobs that trigger calls to the M-Pesa Query API must themselves be protected by appropriate authorization to prevent misuse.
    *   **Rate Limiting:** Be mindful of any rate limits imposed by Safaricom on the Query API and implement internal rate limiting if necessary to avoid being blocked.
    *   **Logging:** Log all query API requests and responses for auditing and debugging.

### 8.6. Logging & Monitoring for M-Pesa Transactions

*   **Explanation:** Comprehensive logging and monitoring are essential for tracking M-Pesa transactions, identifying issues, and investigating potential fraud.
*   **Key Considerations:**
    *   **Log STK Push Initiations:** Record details of every STK push attempt (target phone, amount, `MerchantRequestID`, `CheckoutRequestID`, initial M-Pesa response).
    *   **Log Incoming Callbacks:** Log the full payload and source IP address of every incoming M-Pesa callback request, regardless of whether it's deemed valid or not initially. This helps in identifying spoofing attempts or unexpected callback sources.
    *   **Log Callback Processing Outcomes:** Log the result of callback validation (success, failure reasons) and the subsequent updates made to `MpesaPaymentLog` and `Payment` records.
    *   **Log Query API Calls:** Log requests and responses for any calls made to the M-Pesa Transaction Status Query API.
    *   **Alerts:** Configure alerts for:
        *   High rates of STK push failures.
        *   Callbacks received from unexpected IP addresses (if whitelisting is in place).
        *   Callback validation errors (e.g., mismatched amounts, invalid `CheckoutRequestID`).
        *   Potential duplicate callback processing attempts (if idempotency checks fail).
        *   Failures in calling the M-Pesa Query API.
        *   Unusually high numbers of `TIMEOUT_AWAITING_CALLBACK` statuses.
    *   **Regular Reconciliation:** While not strictly a security design point, advise landlords or implement system features to support reconciliation of M-Pesa statements with system payment records.

## 9. Infrastructure & Operational Security (High-Level)

This section outlines high-level principles and practices for securing the underlying infrastructure and ongoing operations of the Kenyan Rental Management System.

### 9.1. Infrastructure Security Principles

#### 9.1.1. Secure Cloud Provider & Configuration

*   **Explanation:** Leveraging a reputable cloud provider (e.g., AWS, Azure, GCP) offers a strong foundation, but secure configuration of services is paramount.
*   **Key Considerations:**
    *   **Provider Selection:** Choose a provider with robust security offerings, compliance certifications relevant to Kenya (e.g., ISO 27001, PCI DSS if applicable), and data centers that can meet data sovereignty requirements (e.g., DPA 2019).
    *   **Provider Security Tools:** Utilize built-in security tools and services offered by the cloud provider (e.g., security groups, WAF, key management, identity and access management).
    *   **Secure Service Configurations:** Ensure all deployed services (compute instances, databases, storage, networking) are configured securely according to best practices and vendor recommendations. Disable unused services or features.
    *   **Identity and Access Management (IAM):** Implement strict IAM policies to control access to cloud resources, adhering to the principle of least privilege. Use roles rather than individual user credentials for service access where possible. Enforce MFA for all administrative cloud accounts.

#### 9.1.2. Network Security

*   **Explanation:** Protecting the network perimeter and segmenting internal network traffic to limit the blast radius of potential security breaches.
*   **Key Considerations:**
    *   **Virtual Private Cloud (VPC) / Virtual Network:** Deploy the application within an isolated VPC or virtual network.
    *   **Firewalls / Security Groups / Network ACLs:** Implement firewalls (e.g., cloud provider security groups, network ACLs, Web Application Firewall - WAF) to filter traffic at various layers, allowing only necessary ports and protocols from trusted sources.
    *   **Network Segmentation:** Segment the network into different zones (e.g., public DMZ for web servers, private subnet for application servers, separate private subnet for databases). Restrict traffic flow between zones based on the principle of least privilege.
    *   **Intrusion Detection/Prevention Systems (IDS/IPS):** Consider deploying IDS/IPS solutions to detect and potentially block malicious network activity. Many cloud WAFs offer these capabilities.
    *   **DDoS Protection:** Utilize DDoS mitigation services (often provided by cloud providers or specialized vendors) to protect against volumetric and application-layer denial-of-service attacks.

#### 9.1.3. Server/Host Security (OS Hardening)

*   **Explanation:** Securing the operating systems of all servers (virtual machines, containers) that host the application and its components.
*   **Key Considerations:**
    *   **Secure Base Images:** Use hardened, minimal OS base images. Remove unnecessary software, services, and user accounts.
    *   **Regular Patch Management:** Implement a robust patch management process to promptly apply security updates to the OS and installed software. Automate where possible.
    *   **Strict User Access Control:** Limit direct server access. Use SSH keys instead of passwords for administrative access. Implement bastion hosts or jump servers for controlled access to private networks. Enforce MFA for server access.
    *   **Host-Based Firewalls:** Configure host-based firewalls (e.g., iptables, ufw, Windows Firewall) on each server as an additional layer of network control.
    *   **File Integrity Monitoring (FIM):** Consider FIM solutions to detect unauthorized changes to critical system files and configurations.
    *   **Endpoint Detection and Response (EDR):** For larger deployments, EDR solutions can provide advanced threat detection and response capabilities on hosts.

#### 9.1.4. Database Security

*   **Explanation:** Protecting the confidentiality, integrity, and availability of data stored in databases.
*   **Key Considerations:**
    *   **Private Network Placement:** Place database servers in private network subnets, not directly exposed to the internet. Access should be restricted to application servers.
    *   **Strong Unique Credentials:** Use strong, unique credentials for database access. Avoid default usernames/passwords. Application services should use unique, least-privilege database accounts.
    *   **Least Privilege for DB Users:** Database users (including application service accounts) should only have the minimum necessary permissions on specific databases, tables, or views.
    *   **Database Auditing/Logging:** Enable database auditing and logging to track access, DDL changes, and DML changes to sensitive tables.
    *   **Patching:** Keep database software patched and up-to-date.
    *   **Secure Backups:** Ensure database backups are encrypted and stored securely (see section 9.2.5).
    *   **Encryption at Rest:** Utilize TDE and consider ALE for sensitive data within the database (see section 6.1.2).

### 9.2. Operational Security Practices

#### 9.2.1. Change Management

*   **Explanation:** A formal process for managing changes to the production environment to minimize disruptions and security regressions.
*   **Key Considerations:**
    *   **Formal Process:** All changes (code, configuration, infrastructure) must go through a documented change request and approval process.
    *   **Staging & Testing:** Thoroughly test changes in a staging environment that mirrors production before deployment.
    *   **Rollback Plans:** Have well-defined rollback plans in case a change introduces issues.
    *   **Peer Review:** Changes should be reviewed by at least one other qualified individual.

#### 9.2.2. Vulnerability Management

*   **Explanation:** Continuously identifying, assessing, and remediating vulnerabilities in the system and infrastructure.
*   **Key Considerations:**
    *   **Regular Scanning:** Conduct regular automated vulnerability scanning of networks, hosts, and the application (web and API).
    *   **Penetration Testing:** Perform periodic penetration tests (internal and/or third-party) to simulate real-world attacks.
    *   **Patch Prioritization:** Prioritize patching based on vulnerability severity (e.g., CVSS score), exploitability, and potential impact on critical assets.
    *   **Remediation Tracking:** Track identified vulnerabilities and their remediation status.

#### 9.2.3. Monitoring, Logging, and Alerting (Security Focus)

*   **Explanation:** Continuous monitoring of security logs and system activity to detect and respond to potential security incidents.
*   **Key Considerations:**
    *   **Centralized Security Logs:** Aggregate security logs from all relevant sources (servers, firewalls, applications, databases, IDS/IPS) into a centralized Security Information and Event Management (SIEM) system or log management platform.
    *   **Suspicious Activity Monitoring:** Actively monitor for unusual login patterns, unauthorized access attempts, policy violations, malware indicators, and other signs of compromise.
    *   **Real-Time Alerts:** Configure real-time alerts for critical security incidents to enable prompt investigation and response by the security team or designated personnel.

#### 9.2.4. Incident Response Plan

*   **Explanation:** A documented plan outlining the procedures to follow in the event of a security incident (e.g., data breach, DoS attack, malware infection).
*   **Key Considerations:**
    *   **Roles & Responsibilities:** Clearly define roles, responsibilities, and communication channels for the incident response team.
    *   **Phases:** The plan should cover all phases of incident response: Preparation, Identification, Containment, Eradication, Recovery, and Lessons Learned.
    *   **Playbooks:** Develop playbooks for common incident types.
    *   **Testing & Updates:** Regularly test and update the incident response plan through tabletop exercises or simulations.

#### 9.2.5. Backup and Disaster Recovery (BDR)

*   **Explanation:** Ensuring data can be recovered and critical system functions can be restored in the event of data loss, corruption, or a major outage.
*   **Key Considerations:**
    *   **Regular Automated Backups:** Implement regular, automated backups of all critical data (databases, application code, configuration files, uploaded files).
    *   **Secure Storage:** Store backups securely, preferably in a geographically separate location (e.g., different availability zone or region in the cloud) from the primary systems.
    *   **Encryption of Backups:** Encrypt backup data both in transit and at rest.
    *   **Regular Recovery Testing:** Periodically test the data recovery process to ensure backups are valid and can be restored within defined Recovery Time Objectives (RTO).
    *   **Disaster Recovery (DR) Plan:** Develop a DR plan outlining procedures to restore critical system functionality at an alternate site if the primary site becomes unavailable, with defined Recovery Point Objectives (RPO).

#### 9.2.6. Security Awareness Training

*   **Explanation:** Educating all personnel (developers, operations, support, admin staff) about security threats, policies, and their responsibilities in protecting system and data security.
*   **Key Considerations:**
    *   **Regular Training:** Conduct security awareness training at onboarding and periodically thereafter (e.g., annually).
    *   **Relevant Topics:** Cover topics such as phishing, social engineering, password security, secure data handling, incident reporting, and relevant policies (e.g., Data Protection Act compliance).
    *   **Role-Specific Training:** Provide more detailed, role-specific security training for developers (secure coding practices) and system administrators (secure system configuration and management).
    *   **Updates:** Update training content regularly to address new threats and evolving best practices.
