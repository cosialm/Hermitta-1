from enum import Enum
from datetime import datetime, date
from typing import Optional, Dict, Any, List
from decimal import Decimal

# Phase 6: Advanced Integrations & Scalability (with MFA additions)
class UserRole(Enum):
    LANDLORD = "LANDLORD"
    TENANT = "TENANT"
    STAFF = "STAFF"
    VENDOR = "VENDOR"
    ACCOUNTANT = "ACCOUNTANT"
    ADMIN = "ADMIN"

class PreferredLoginMethod(Enum):
    EMAIL = "EMAIL"
    PHONE = "PHONE"

class PreferredLanguage(Enum):
    EN_KE = "en_KE"
    SW_KE = "sw_KE"

VENDOR_SERVICE_EXAMPLES = ["PLUMBING", "ELECTRICAL", "CLEANING", "SECURITY_SERVICES", "HVAC_REPAIR", "PAINTING"]

class User:
    def __init__(self,
                 user_id: int,
                 email: str,
                 phone_number: str,
                 password_hash: str,
                 first_name: str,
                 last_name: str,
                 role: UserRole,
                 is_phone_verified: bool = False,
                 phone_verification_otp: Optional[str] = None,
                 phone_verification_otp_expires_at: Optional[datetime] = None,
                 kra_pin: Optional[str] = None,
                 preferred_login_method: PreferredLoginMethod = PreferredLoginMethod.EMAIL,
                 preferred_language: PreferredLanguage = PreferredLanguage.EN_KE,
                 last_consent_review_date: Optional[date] = None,
                 data_processing_consent_details: Optional[Dict[str, Any]] = None,
                 company_name: Optional[str] = None,
                 staff_permissions: Optional[Dict[str, Any]] = None,
                 # Vendor-specific fields
                 vendor_services_offered: Optional[List[str]] = None,
                 vendor_rating_average: Optional[Decimal] = None, # Overall average rating score
                 vendor_total_ratings_count: Optional[int] = 0,  # Total number of ratings received
                 is_verified_vendor: bool = False,
                 # MFA Fields:
                 otp_secret: Optional[str] = None, # Encrypted secret for TOTP
                 is_mfa_enabled: bool = False, # User has MFA enabled
                 otp_backup_codes: Optional[List[str]] = None, # List of one-time hashed recovery codes
                 is_active: bool = True,
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.user_id = user_id
        self.email = email
        self.phone_number = phone_number
        self.password_hash = password_hash # Must be securely hashed (e.g., Argon2, bcrypt)
        self.first_name = first_name
        self.last_name = last_name
        self.role = role

        self.is_phone_verified = is_phone_verified
        self.phone_verification_otp = phone_verification_otp # Store hashed if sensitive, or one-time use
        self.phone_verification_otp_expires_at = phone_verification_otp_expires_at

        if self.role == UserRole.LANDLORD:
            self.kra_pin = kra_pin
        else:
            self.kra_pin = None

        self.preferred_login_method = preferred_login_method
        self.preferred_language = preferred_language
        self.last_consent_review_date = last_consent_review_date
        self.data_processing_consent_details = data_processing_consent_details if data_processing_consent_details is not None else {}

        self.company_name = company_name

        if self.role == UserRole.STAFF or self.role == UserRole.ACCOUNTANT:
            self.staff_permissions = staff_permissions if staff_permissions is not None else {}
        else:
            self.staff_permissions = {}

        if self.role == UserRole.VENDOR:
            self.vendor_services_offered = vendor_services_offered if vendor_services_offered is not None else []
            self.vendor_rating_average = vendor_rating_average # This will be calculated and updated
            self.vendor_total_ratings_count = vendor_total_ratings_count if vendor_total_ratings_count is not None else 0
            self.is_verified_vendor = is_verified_vendor
        else:
            self.vendor_services_offered = []
            self.vendor_rating_average = None
            self.vendor_total_ratings_count = 0
            self.is_verified_vendor = False

        # MFA details
        self.otp_secret = otp_secret # Encrypt this before storing
        self.is_mfa_enabled = is_mfa_enabled
        self.otp_backup_codes = otp_backup_codes if otp_backup_codes is not None else [] # Store hashed codes

        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

    # Placeholder methods for handling encrypted MFA secret (actual logic elsewhere)
    def get_otp_secret(self) -> Optional[str]:
        # TODO: Implement decryption of self.otp_secret
        return self.otp_secret

    def set_otp_secret(self, plain_secret: str):
        # TODO: Implement encryption then set self.otp_secret
        self.otp_secret = plain_secret # Placeholder

# Example Usage (Phase 6 with MFA):
# admin_user = User(user_id=5, email="admin@example.com", phone_number="+2547ADMIN000", password_hash="...",
#                   first_name="Sys", last_name="Admin", role=UserRole.ADMIN,
#                   is_mfa_enabled=True, otp_secret="encrypted_super_secret",
#                   otp_backup_codes=["hashed_code1", "hashed_code2"])
# print(admin_user.role, admin_user.is_mfa_enabled)
