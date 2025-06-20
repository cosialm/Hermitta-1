from enum import Enum
from datetime import datetime, date
from typing import Optional, Dict, Any, List # Added List for services/permissions
from decimal import Decimal # Added for vendor_rating_average

# Phase 6: Advanced Integrations & Scalability (Builds on Phase 5 state)
class UserRole(Enum):
    LANDLORD = "LANDLORD"
    TENANT = "TENANT"
    STAFF = "STAFF"         # Platform staff or Landlord's staff
    VENDOR = "VENDOR"       # External service provider (plumber, electrician)
    ACCOUNTANT = "ACCOUNTANT" # Specialized role for financial access (can be a type of STAFF)
    ADMIN = "ADMIN"         # System super administrator

class PreferredLoginMethod(Enum):
    EMAIL = "EMAIL"
    PHONE = "PHONE"

class PreferredLanguage(Enum):
    EN_KE = "en_KE"
    SW_KE = "sw_KE"

# Example vendor services - could be a separate ServiceCategory model later
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
                 # Phase 6 Enhancements for Staff/Vendor:
                 company_name: Optional[str] = None, # For VENDOR (e.g., "Joe's Plumbing") or STAFF (department/team)
                 staff_permissions: Optional[Dict[str, Any]] = None, # JSON for STAFF, e.g. {"can_access_all_properties": false, "property_ids": [1,2]}
                 # For VENDOR role:
                 vendor_services_offered: Optional[List[str]] = None, # List of service strings or FKs to ServiceCategory model
                 vendor_rating_average: Optional[Decimal] = None, # Calculated from reviews/feedback
                 is_verified_vendor: bool = False, # Platform or landlord verified
                 # For STAFF role (manages_property_ids was from initial P6 outline, staff_permissions is more flexible)
                 # manages_property_ids: Optional[List[int]] = None,
                 is_active: bool = True,
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.user_id = user_id
        self.email = email
        self.phone_number = phone_number
        self.password_hash = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.role = role

        self.is_phone_verified = is_phone_verified
        self.phone_verification_otp = phone_verification_otp
        self.phone_verification_otp_expires_at = phone_verification_otp_expires_at

        if self.role == UserRole.LANDLORD:
            self.kra_pin = kra_pin
        else:
            self.kra_pin = None # Not applicable or not enforced for other roles initially

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
            self.vendor_rating_average = vendor_rating_average
            self.is_verified_vendor = is_verified_vendor
        else:
            self.vendor_services_offered = []
            self.vendor_rating_average = None
            self.is_verified_vendor = False

        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage (Phase 6):
# staff_user_p6 = User(user_id=3, email="staff@example.com", phone_number="+254700000003", password_hash="...",
#                      first_name="Staff", last_name="Member", role=UserRole.STAFF,
#                      staff_permissions={"can_view_maintenance_all": True, "can_edit_leases_prop_ids": [101, 102]})
#
# vendor_user_p6 = User(user_id=4, email="plumbingco@example.com", phone_number="+254700000004", password_hash="...",
#                       first_name="Peter", last_name="Plumber", role=UserRole.VENDOR,
#                       company_name="Reliable Plumbers Ltd.",
#                       vendor_services_offered=["PLUMBING", "DRAINAGE_CLEANING"],
#                       is_verified_vendor=True, vendor_rating_average=Decimal("4.5"))
# print(staff_user_p6.role, staff_user_p6.staff_permissions)
# print(vendor_user_p6.company_name, vendor_user_p6.vendor_services_offered)
