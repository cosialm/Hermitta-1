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

# Remove local enum definitions as they are now in models.enums
# class AuditActionCategory(Enum): ...
# class AuditActionStatus(Enum): ...
# class AuditActionType(Enum): ...

from hermitta_app import db # Import db instance
from .enums import AuditLogEvent, AuditActionCategory, AuditActionStatus # Import enums

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    log_id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    event_type = db.Column(db.Enum(AuditLogEvent), nullable=False, index=True) # Changed from action_type

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True, index=True)

    action_category = db.Column(db.Enum(AuditActionCategory), nullable=True, index=True)

    details = db.Column(db.JSON, nullable=True) # Consolidated field

    target_entity_type = db.Column(db.String(100), nullable=True, index=True)
    target_entity_id = db.Column(db.String(100), nullable=True, index=True) # Using String to accommodate various ID types

    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)

    status = db.Column(db.Enum(AuditActionStatus), default=AuditActionStatus.SUCCESS, nullable=True, index=True)

    # Relationships
    user = db.relationship('User', backref=db.backref('performed_audit_logs', lazy='dynamic')) # Changed backref name

    def __init__(self, **kwargs):
        # Explicitly set default for status if not provided, to ensure it's set before commit
        if 'status' not in kwargs:
            kwargs['status'] = AuditActionStatus.SUCCESS
        super().__init__(**kwargs)

    def __repr__(self):
        return f"<AuditLog {self.log_id} - User: {self.user_id}, Event: {self.event_type.value}>"

# Example Usage (SQLAlchemy style):
# log_entry = AuditLog(
#     user_id=10,
#     event_type=AuditLogEvent.ENTITY_UPDATED,
#     action_category=AuditActionCategory.PROPERTY_MANAGEMENT,
#     target_entity_type="Property",
#     target_entity_id="101",
#     details={"change_summary": "Rent amount updated", "old_values": {"rent_amount": 50000}, "new_values": {"rent_amount": 52000}},
#     ip_address="192.168.1.100",
#     status=AuditActionStatus.SUCCESS
# )
# db.session.add(log_entry)
# db.session.commit()
