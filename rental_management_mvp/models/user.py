from enum import Enum
from datetime import datetime
from typing import Optional

# Refined for Phase 1 MVP
class UserRole(Enum):
    LANDLORD = "LANDLORD"
    TENANT = "TENANT"

class PreferredLoginMethod(Enum):
    EMAIL = "EMAIL"
    PHONE = "PHONE"

class User:
    def __init__(self,
                 user_id: int,
                 email: str, # Unique, Indexed
                 phone_number: str, # Unique, Indexed, Mandatory for this refined MVP
                 password_hash: str,
                 first_name: str,
                 last_name: str,
                 role: UserRole,
                 is_phone_verified: bool = False,
                 phone_verification_otp: Optional[str] = None,
                 phone_verification_otp_expires_at: Optional[datetime] = None,
                 kra_pin: Optional[str] = None, # Optional, Indexed, for Landlords
                 preferred_login_method: PreferredLoginMethod = PreferredLoginMethod.EMAIL,
                 is_active: bool = True, # Default to active, admin can deactivate
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
            self.kra_pin = kra_pin # KRA PIN only applicable to Landlords
        else:
            self.kra_pin = None

        self.preferred_login_method = preferred_login_method
        self.is_active = is_active # To allow deactivation of users

        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage (Refined Phase 1):
# landlord = User(user_id=1, email="landlord@example.co.ke", phone_number="+254712345678",
#                 password_hash="hashed_pw", first_name="Mary", last_name="Landlord",
#                 role=UserRole.LANDLORD, kra_pin="A123456789Z",
#                 preferred_login_method=PreferredLoginMethod.EMAIL)
#
# tenant_with_phone_login = User(user_id=2, email="tenant@example.co.ke", phone_number="+254798765432",
#                                password_hash="hashed_pw2", first_name="John", last_name="Tenant",
#                                role=UserRole.TENANT,
#                                preferred_login_method=PreferredLoginMethod.PHONE,
#                                is_phone_verified=True)
#
# print(landlord.email, landlord.kra_pin)
# print(tenant_with_phone_login.phone_number, tenant_with_phone_login.preferred_login_method)
