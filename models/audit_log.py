from enum import Enum
from datetime import datetime
from typing import Optional, Dict, Any, Union # Union for target_entity_id

# It's good practice to ensure User model is defined before this if using direct FK type hinting
# from .user import User # Assuming User model is in user.py in the same directory

class AuditActionCategory(Enum): # Broad categories for filtering/grouping
    AUTHENTICATION = "AUTHENTICATION"
    USER_MANAGEMENT = "USER_MANAGEMENT"
    PROPERTY_MANAGEMENT = "PROPERTY_MANAGEMENT"
    LEASE_MANAGEMENT = "LEASE_MANAGEMENT"
    FINANCIAL_MANAGEMENT = "FINANCIAL_MANAGEMENT"
    MAINTENANCE_MANAGEMENT = "MAINTENANCE_MANAGEMENT"
    DOCUMENT_MANAGEMENT = "DOCUMENT_MANAGEMENT"
    COMMUNICATION = "COMMUNICATION"
    SYSTEM_CONFIGURATION = "SYSTEM_CONFIGURATION"
    SECURITY_EVENT = "SECURITY_EVENT"
    ADMIN_ACTION = "ADMIN_ACTION"
    OTHER = "OTHER"

class AuditActionStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    PENDING = "PENDING" # For actions that might be async

# Example Specific Action Types (can be expanded significantly)
# These could also be more structured, e.g. by combining a general action (CREATE, UPDATE, DELETE)
# with an entity type. For simplicity, a flat enum is shown here.
class AuditActionType(Enum):
    # Authentication
    USER_LOGIN_SUCCESS = "USER_LOGIN_SUCCESS"
    USER_LOGIN_FAILURE = "USER_LOGIN_FAILURE"
    USER_LOGOUT = "USER_LOGOUT"
    USER_PASSWORD_RESET_REQUEST = "USER_PASSWORD_RESET_REQUEST"
    USER_PASSWORD_RESET_SUCCESS = "USER_PASSWORD_RESET_SUCCESS"
    USER_MFA_SETUP_INITIATED = "USER_MFA_SETUP_INITIATED"
    USER_MFA_SETUP_COMPLETED = "USER_MFA_SETUP_COMPLETED"
    USER_MFA_CHALLENGE_SUCCESS = "USER_MFA_CHALLENGE_SUCCESS"
    USER_MFA_CHALLENGE_FAILURE = "USER_MFA_CHALLENGE_FAILURE"
    USER_MFA_RECOVERY_CODE_USED = "USER_MFA_RECOVERY_CODE_USED"

    # User Management
    USER_CREATED = "USER_CREATED" # By admin or self-registration
    USER_UPDATED_PROFILE = "USER_UPDATED_PROFILE"
    USER_ROLE_CHANGED = "USER_ROLE_CHANGED" # Admin action
    USER_ACCOUNT_ACTIVATED = "USER_ACCOUNT_ACTIVATED" # Admin action
    USER_ACCOUNT_DEACTIVATED = "USER_ACCOUNT_DEACTIVATED" # Admin action
    USER_CONSENT_UPDATED = "USER_CONSENT_UPDATED"

    # Property Management
    PROPERTY_CREATED = "PROPERTY_CREATED"
    PROPERTY_UPDATED = "PROPERTY_UPDATED"
    PROPERTY_DELETED = "PROPERTY_DELETED"
    PROPERTY_LISTING_UPDATED = "PROPERTY_LISTING_UPDATED"

    # Lease Management
    LEASE_CREATED = "LEASE_CREATED"
    LEASE_UPDATED = "LEASE_UPDATED"
    LEASE_TERMINATED = "LEASE_TERMINATED" # Could be early termination or end of term
    LEASE_DOCUMENT_UPLOADED = "LEASE_DOCUMENT_UPLOADED"
    LEASE_SIGNATURE_REQUEST_SENT = "LEASE_SIGNATURE_REQUEST_SENT"
    LEASE_SIGNED_BY_PARTY = "LEASE_SIGNED_BY_PARTY"
    LEASE_FULLY_SIGNED = "LEASE_FULLY_SIGNED"

    # Financial Management
    PAYMENT_MANUAL_RECORDED = "PAYMENT_MANUAL_RECORDED"
    PAYMENT_MPESA_INITIATED = "PAYMENT_MPESA_INITIATED"
    PAYMENT_MPESA_CALLBACK_RECEIVED = "PAYMENT_MPESA_CALLBACK_RECEIVED"
    PAYMENT_MPESA_CALLBACK_SUCCESS = "PAYMENT_MPESA_CALLBACK_SUCCESS"
    PAYMENT_MPESA_CALLBACK_FAILURE = "PAYMENT_MPESA_CALLBACK_FAILURE"
    FINANCIAL_TRANSACTION_CREATED = "FINANCIAL_TRANSACTION_CREATED"
    FINANCIAL_TRANSACTION_UPDATED = "FINANCIAL_TRANSACTION_UPDATED"
    FINANCIAL_TRANSACTION_DELETED = "FINANCIAL_TRANSACTION_DELETED"
    MPESA_CONFIG_CREATED = "MPESA_CONFIG_CREATED"
    MPESA_CONFIG_UPDATED = "MPESA_CONFIG_UPDATED"
    BUDGET_CREATED = "BUDGET_CREATED"
    BUDGET_UPDATED = "BUDGET_UPDATED"
    BUDGET_DELETED = "BUDGET_DELETED"

    # Maintenance
    MAINTENANCE_REQUEST_CREATED = "MAINTENANCE_REQUEST_CREATED"
    MAINTENANCE_REQUEST_STATUS_UPDATED = "MAINTENANCE_REQUEST_STATUS_UPDATED"
    MAINTENANCE_REQUEST_ASSIGNED = "MAINTENANCE_REQUEST_ASSIGNED"
    MAINTENANCE_QUOTE_SUBMITTED = "MAINTENANCE_QUOTE_SUBMITTED"
    MAINTENANCE_QUOTE_STATUS_UPDATED = "MAINTENANCE_QUOTE_STATUS_UPDATED" # Approved/Rejected
    MAINTENANCE_INVOICE_SUBMITTED = "MAINTENANCE_INVOICE_SUBMITTED"
    MAINTENANCE_INVOICE_STATUS_UPDATED = "MAINTENANCE_INVOICE_STATUS_UPDATED" # Paid/Approved

    # Document Management
    DOCUMENT_UPLOADED = "DOCUMENT_UPLOADED"
    DOCUMENT_VIEWED = "DOCUMENT_VIEWED" # Can be noisy, use with caution or for sensitive docs
    DOCUMENT_SHARED = "DOCUMENT_SHARED"
    DOCUMENT_SHARE_REVOKED = "DOCUMENT_SHARE_REVOKED"
    DOCUMENT_DELETED = "DOCUMENT_DELETED"
    DOCUMENT_FOLDER_CREATED = "DOCUMENT_FOLDER_CREATED"
    DOCUMENT_FOLDER_DELETED = "DOCUMENT_FOLDER_DELETED"

    # Admin / System
    ADMIN_USER_IMPERSONATION_STARTED = "ADMIN_USER_IMPERSONATION_STARTED"
    ADMIN_USER_IMPERSONATION_ENDED = "ADMIN_USER_IMPERSONATION_ENDED"
    ADMIN_PLATFORM_SETTING_CHANGED = "ADMIN_PLATFORM_SETTING_CHANGED" # e.g. Notification Template updated
    ADMIN_USER_SUSPENDED = "ADMIN_USER_SUSPENDED" # Covered by USER_ACCOUNT_DEACTIVATED
    ADMIN_EXPORTED_USER_DATA = "ADMIN_EXPORTED_USER_DATA" # DSAR related

    # Security
    SECURITY_UNAUTHORIZED_ACCESS_ATTEMPT = "SECURITY_UNAUTHORIZED_ACCESS_ATTEMPT"
    SECURITY_CALLBACK_VALIDATION_FAILURE = "SECURITY_CALLBACK_VALIDATION_FAILURE" # e.g. M-Pesa callback

class AuditLog:
    def __init__(self,
                 log_id: int, # Primary Key, Auto-incrementing Integer
                 timestamp: datetime, # Auto now add, when the log entry was created
                 action_type: AuditActionType, # What action was performed
                 user_id: Optional[int] = None, # FK to User model, Nullable if system-initiated
                 target_entity_type: Optional[str] = None, # e.g., "User", "Property", "Lease"
                 target_entity_id: Optional[Union[int, str]] = None, # ID of the affected entity
                 details_before: Optional[Dict[str, Any]] = None, # JSON snapshot of data before change (for UPDATEs)
                 details_after: Optional[Dict[str, Any]] = None,  # JSON snapshot of data after change (for CREATEs/UPDATEs)
                 ip_address: Optional[str] = None,
                 user_agent: Optional[str] = None,
                 status: Optional[AuditActionStatus] = AuditActionStatus.SUCCESS, # e.g., for login attempts or actions that can fail
                 failure_reason: Optional[str] = None, # If status is FAILURE
                 # Optional: A broader category for easier filtering, can be derived from action_type
                 action_category: Optional[AuditActionCategory] = None,
                 notes: Optional[str] = None # Any additional context or notes for this log entry
                 ):

        self.log_id = log_id
        self.user_id = user_id # The user who performed the action, or system if None
        self.timestamp = timestamp
        self.action_type = action_type
        self.action_category = action_category # Can be auto-set based on action_type

        self.target_entity_type = target_entity_type
        self.target_entity_id = target_entity_id # Can be int or string (e.g. for string-based IDs if any)

        # Storing JSON diffs can be very powerful but also storage-intensive.
        # For sensitive fields, ensure they are masked or not logged in detail_before/after if too risky.
        self.details_before = details_before
        self.details_after = details_after

        self.ip_address = ip_address
        self.user_agent = user_agent

        self.status = status
        self.failure_reason = failure_reason
        self.notes = notes

# Example Usage:
# log_entry = AuditLog(
#     log_id=1, # Auto-incremented in a real DB
#     timestamp=datetime.utcnow(),
#     user_id=10, # Landlord User ID
#     action_type=AuditActionType.PROPERTY_UPDATED,
#     action_category=AuditActionCategory.PROPERTY_MANAGEMENT,
#     target_entity_type="Property",
#     target_entity_id=101,
#     details_before={"rent_amount": 50000, "status": "VACANT"},
#     details_after={"rent_amount": 52000, "status": "LISTED"},
#     ip_address="192.168.1.100",
#     user_agent="Mozilla/5.0 ...",
#     status=AuditActionStatus.SUCCESS
# )
#
# login_failure_log = AuditLog(
#     log_id=2, timestamp=datetime.utcnow(), user_id=None, # User ID might be unknown or not yet authenticated
#     action_type=AuditActionType.USER_LOGIN_FAILURE,
#     action_category=AuditActionCategory.AUTHENTICATION,
#     details_before={"attempted_email": "unknown_user@example.com"}, # Don't log password attempt
#     ip_address="203.0.113.45",
#     status=AuditActionStatus.FAILURE,
#     failure_reason="Invalid credentials"
# )
# print(log_entry.action_type, log_entry.target_entity_id)
