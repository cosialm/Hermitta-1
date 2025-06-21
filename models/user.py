import enum # Use standard enum for SQLAlchemy
from datetime import datetime, date
from typing import Optional, Dict, Any, List # Keep for type hinting if needed elsewhere
from decimal import Decimal
from hermitta_app import db # Import db instance

# Phase 6: Advanced Integrations & Scalability (with MFA additions)
# Enums remain the same, but ensure they are standard Python enums
class UserRole(enum.Enum):
    LANDLORD = "LANDLORD"
    TENANT = "TENANT"
    STAFF = "STAFF"
    VENDOR = "VENDOR"
    ACCOUNTANT = "ACCOUNTANT"
    ADMIN = "ADMIN"

class PreferredLoginMethod(enum.Enum):
    EMAIL = "EMAIL"
    PHONE = "PHONE"

class PreferredLanguage(enum.Enum):
    EN_KE = "en_KE"
    SW_KE = "sw_KE"

VENDOR_SERVICE_EXAMPLES = ["PLUMBING", "ELECTRICAL", "CLEANING", "SECURITY_SERVICES", "HVAC_REPAIR", "PAINTING"]

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False) # Increased length for stronger hashes
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.TENANT)

    is_phone_verified = db.Column(db.Boolean, default=False, nullable=False)
    phone_verification_otp = db.Column(db.String(10), nullable=True) # Store hashed if sensitive
    phone_verification_otp_expires_at = db.Column(db.DateTime, nullable=True)

    kra_pin = db.Column(db.String(20), nullable=True, index=True) # Specific to LANDLORD role

    preferred_login_method = db.Column(db.Enum(PreferredLoginMethod), default=PreferredLoginMethod.EMAIL, nullable=False)
    preferred_language = db.Column(db.Enum(PreferredLanguage), default=PreferredLanguage.EN_KE, nullable=False)

    last_consent_review_date = db.Column(db.Date, nullable=True)
    data_processing_consent_details = db.Column(db.JSON, nullable=True) # Store as JSON

    company_name = db.Column(db.String(100), nullable=True)
    staff_permissions = db.Column(db.JSON, nullable=True) # Store as JSON, specific to STAFF/ACCOUNTANT

    # Vendor-specific fields
    vendor_services_offered = db.Column(db.JSON, nullable=True) # Store as JSON list of strings
    vendor_rating_average = db.Column(db.Numeric(3, 2), nullable=True) # e.g., 4.75
    vendor_total_ratings_count = db.Column(db.Integer, default=0, nullable=True)
    is_verified_vendor = db.Column(db.Boolean, default=False, nullable=True)

    # MFA Fields
    otp_secret = db.Column(db.String(255), nullable=True) # Encrypted secret for TOTP
    is_mfa_enabled = db.Column(db.Boolean, default=False, nullable=False)
    otp_backup_codes = db.Column(db.JSON, nullable=True) # Store as JSON list of hashed codes

    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships (will be defined as we convert other models)
    # properties = db.relationship('Property', backref='landlord', lazy=True, foreign_keys='Property.landlord_id')
    # leases_as_landlord = db.relationship('Lease', backref='landlord_user', lazy=True, foreign_keys='Lease.landlord_id')
    # leases_as_tenant = db.relationship('Lease', backref='tenant_user', lazy=True, foreign_keys='Lease.tenant_id')
    # maintenance_requests_created = db.relationship('MaintenanceRequest', backref='creator', lazy=True, foreign_keys='MaintenanceRequest.created_by_user_id')
    # maintenance_requests_assigned = db.relationship('MaintenanceRequest', backref='assignee', lazy=True, foreign_keys='MaintenanceRequest.assigned_to_user_id')


    # The __init__ method is largely handled by SQLAlchemy's db.Model.
    # Logic for setting kra_pin based on role, or staff_permissions, etc.,
    # should be handled in the service layer before creating the User instance,
    # or via @validates decorators or model event listeners if strictly model behavior.

    # Placeholder methods for handling encrypted MFA secret (actual logic elsewhere)
    # def get_otp_secret(self) -> Optional[str]:
    #     # TODO: Implement decryption of self.otp_secret
    #     return self.otp_secret

    # def set_otp_secret(self, plain_secret: str):
    #     # TODO: Implement encryption then set self.otp_secret
    #     self.otp_secret = plain_secret # Placeholder

    def __repr__(self):
        return f"<User {self.user_id}: {self.email} ({self.role.value})>"

# Example Usage (Phase 6 with MFA) - This would now be done via db.session.add()
# admin_user_data = {
#     "email": "admin@example.com", "phone_number": "+2547ADMIN000", "password_hash": "hashed_password",
#     "first_name": "Sys", "last_name": "Admin", "role": UserRole.ADMIN,
#     "is_mfa_enabled": True, "otp_secret": "encrypted_super_secret", # Service should encrypt
#     "otp_backup_codes": ["hashed_code1", "hashed_code2"] # Service should hash
# }
# admin_user = User(**admin_user_data)
# # db.session.add(admin_user)
# # db.session.commit()
# # print(admin_user.role, admin_user.is_mfa_enabled)
