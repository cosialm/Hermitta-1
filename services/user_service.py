from typing import List, Optional, Dict, Any
from datetime import datetime, date # date might be needed for User model fields like last_consent_review_date
from decimal import Decimal # For vendor_rating_average
from models.user import User, UserRole, PreferredLoginMethod, PreferredLanguage # Assuming these are in models.user

class UserService:
    def __init__(self):
        self.users: List[User] = []
        self._next_id: int = 1

    def _process_user_data_for_save(self, user_data: Dict[str, Any], is_creation: bool = False) -> Dict[str, Any]:
        """Helper to process enums and other specific fields before User model instantiation or update."""
        processed_data = user_data.copy()

        # Handle enums
        if 'role' in processed_data and isinstance(processed_data['role'], str):
            try:
                processed_data['role'] = UserRole[processed_data['role'].upper()]
            except KeyError:
                raise ValueError(f"Invalid role string: {processed_data['role']}")

        if 'preferred_login_method' in processed_data and isinstance(processed_data['preferred_login_method'], str):
            try:
                processed_data['preferred_login_method'] = PreferredLoginMethod[processed_data['preferred_login_method'].upper()]
            except KeyError:
                raise ValueError(f"Invalid preferred_login_method string: {processed_data['preferred_login_method']}")
        elif is_creation and 'preferred_login_method' not in processed_data:
             processed_data['preferred_login_method'] = PreferredLoginMethod.EMAIL # Default from model

        if 'preferred_language' in processed_data and isinstance(processed_data['preferred_language'], str):
            # Assuming format like "en_KE" matches enum member name if direct mapping, or needs conversion.
            # For direct mapping like EN_KE:
            try:
                processed_data['preferred_language'] = PreferredLanguage[processed_data['preferred_language'].upper()]
            except KeyError:
                # Or try replacing '-' with '_' if format might be en-KE
                try:
                    processed_data['preferred_language'] = PreferredLanguage[processed_data['preferred_language'].replace('-', '_').upper()]
                except KeyError:
                    raise ValueError(f"Invalid preferred_language string: {processed_data['preferred_language']}")
        elif is_creation and 'preferred_language' not in processed_data:
            processed_data['preferred_language'] = PreferredLanguage.EN_KE # Default from model

        # Handle specific fields based on role (especially for creation)
        role_to_check = processed_data.get('role', None) # Role might not be in update_data

        if role_to_check != UserRole.LANDLORD and 'kra_pin' in processed_data:
            if is_creation or (not is_creation and 'role' in processed_data): # if role is changing away from LANDLORD
                processed_data['kra_pin'] = None

        staff_roles = [UserRole.STAFF, UserRole.ACCOUNTANT, UserRole.ADMIN] # ADMIN also staff-like
        if role_to_check not in staff_roles and 'staff_permissions' in processed_data:
            if is_creation or (not is_creation and 'role' in processed_data):
                 processed_data['staff_permissions'] = {}
        elif role_to_check in staff_roles and 'staff_permissions' not in processed_data and is_creation:
            processed_data['staff_permissions'] = {}


        if role_to_check != UserRole.VENDOR:
            vendor_fields_to_clear = ['vendor_services_offered', 'vendor_rating_average', 'vendor_total_ratings_count', 'is_verified_vendor']
            for field in vendor_fields_to_clear:
                if field in processed_data:
                    if is_creation or (not is_creation and 'role' in processed_data):
                        if field == 'vendor_services_offered': processed_data[field] = []
                        elif field == 'vendor_rating_average': processed_data[field] = None
                        elif field == 'vendor_total_ratings_count': processed_data[field] = 0
                        elif field == 'is_verified_vendor': processed_data[field] = False
        elif role_to_check == UserRole.VENDOR and is_creation: # Set defaults for vendor if creating
            if 'vendor_services_offered' not in processed_data: processed_data['vendor_services_offered'] = []
            if 'vendor_rating_average' not in processed_data: processed_data['vendor_rating_average'] = None
            if 'vendor_total_ratings_count' not in processed_data: processed_data['vendor_total_ratings_count'] = 0
            if 'is_verified_vendor' not in processed_data: processed_data['is_verified_vendor'] = False

        if 'vendor_rating_average' in processed_data and processed_data['vendor_rating_average'] is not None:
            processed_data['vendor_rating_average'] = Decimal(str(processed_data['vendor_rating_average']))

        # Defaults for boolean fields if creating
        if is_creation:
            if 'is_phone_verified' not in processed_data: processed_data['is_phone_verified'] = False
            if 'is_mfa_enabled' not in processed_data: processed_data['is_mfa_enabled'] = False
            if 'is_active' not in processed_data: processed_data['is_active'] = True
            if 'otp_backup_codes' not in processed_data : processed_data['otp_backup_codes'] = []


        # For password_hash, assume it's pre-hashed. For otp_secret, store as is for stub.
        return processed_data

    def create_user(self, user_data: Dict[str, Any]) -> User:
        new_user_id = self._next_id

        # Process data (enums, role-specific logic, defaults)
        processed_data = self._process_user_data_for_save(user_data, is_creation=True)
        processed_data["user_id"] = new_user_id

        # Ensure required fields for User model are present
        # User model __init__ handles created_at/updated_at defaults
        try:
            # For stub simplicity, if password_hash is not provided but password is, use password as hash
            if 'password' in processed_data and 'password_hash' not in processed_data:
                processed_data['password_hash'] = processed_data.pop('password')

            user_instance = User(**processed_data)
        except TypeError as e:
            raise ValueError(f"Missing required fields or incorrect data for User creation: {e}")
        except Exception as e:
            raise ValueError(f"Error during User instantiation: {e}")

        self.users.append(user_instance)
        self._next_id += 1
        return user_instance

    def get_user(self, user_id: int) -> Optional[User]:
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def get_user_by_id(self, user_id: int) -> Optional[User]: # Alias for route tests
        return self.get_user(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        for user in self.users:
            if user.email.lower() == email.lower():
                return user
        return None

    def get_user_by_token(self, token: str) -> Optional[User]: # Used in auth_routes tests
        # Dummy: in real app, token is validated and user fetched.
        # For stub, assume token is user_id as string.
        try:
            user_id = int(token)
            return self.get_user(user_id)
        except ValueError:
            return None


    def update_user(self, user_id: int, update_data: Dict[str, Any]) -> Optional[User]:
        user_to_update = self.get_user(user_id)
        if user_to_update:
            # Get current role before processing update_data, in case role itself is being changed
            current_role = user_to_update.role
            if 'role' in update_data and isinstance(update_data['role'], str):
                try:
                    current_role = UserRole[update_data['role'].upper()] # Use the new role for processing
                except KeyError:
                    raise ValueError(f"Invalid role string in update: {update_data['role']}")
            elif 'role' in update_data and isinstance(update_data['role'], UserRole):
                current_role = update_data['role']


            processed_data = self._process_user_data_for_save({**update_data, 'role': current_role}, is_creation=False)

            for key, value in processed_data.items():
                if hasattr(user_to_update, key):
                    # Special handling if password is provided for update (means password_hash should be updated)
                    if key == 'password' and 'password_hash' not in processed_data:
                        setattr(user_to_update, 'password_hash', value) # Store as "hash"
                    else:
                        setattr(user_to_update, key, value)

            # If role was changed and new role is not LANDLORD, ensure kra_pin is None
            if 'role' in processed_data and user_to_update.role != UserRole.LANDLORD:
                user_to_update.kra_pin = None

            user_to_update.updated_at = datetime.utcnow()
            return user_to_update
        return None

    def delete_user(self, user_id: int) -> bool:
        user_to_delete = self.get_user(user_id)
        if user_to_delete:
            self.users.remove(user_to_delete)
            return True
        return False

    def verify_credentials(self, email: str, password_to_check: str) -> Optional[User]:
        user = self.get_user_by_email(email)
        if user:
            # Stub logic: Direct comparison. Real service uses bcrypt.checkpw().
            # Assumes password_hash stores the plain password for this stub.
            if user.password_hash == password_to_check:
                return user
        return None

    def reset_password_for_user(self, user: User, new_password: str) -> bool: # Used in auth_routes tests
        # This is a conceptual method that auth_routes might call.
        # It assumes 'user' is a User object.
        if user and isinstance(user, User) and self.get_user(user.user_id): # Check if user is in our list
            # For stub, directly set the new "hashed" password
            user.password_hash = new_password
            user.updated_at = datetime.utcnow()
            # In a real scenario, you'd save the user object change to DB.
            # Here, the user object passed in is modified directly.
            return True
        return False

    # Dummy methods for compatibility with other test modules
    def get_current_landlord_id(self): return 1 # Dummy
    def get_current_tenant_user(self): return self.get_user(1) # Dummy, assumes user 1 is a tenant
    def get_current_user_with_roles(self): return self.get_user(1) # Dummy
    def get_current_authenticated_user_id(self): return 1 # Dummy
    def ensure_landlord_permission_for_property(self, landlord_id, property_id): return True # Dummy
    def ensure_admin_role(self): return True # Dummy
    def get_vendor_details_for_rating_list(self, vendor_id: int) : return self.get_user(vendor_id)
    def update_vendor_average_rating_stats(self, vendor_id: int):
        user = self.get_user(vendor_id)
        if user and user.role == UserRole.VENDOR:
            # Dummy logic, real logic would fetch all ratings and calculate
            user.vendor_rating_average = Decimal("4.5")
            user.vendor_total_ratings_count = (user.vendor_total_ratings_count or 0) + 1
            user.updated_at = datetime.utcnow()
            return True
        return False
    def validate_vendor_ids(self, vendor_ids: List[int]): return True # Dummy
    def get_current_vendor_user_id(self): return 1 # Dummy, assumes user 1 is a vendor

# Example Usage
if __name__ == '__main__':
    service = UserService()
    landlord_data = {
        "email": "landlord@example.com", "password_hash": "pass123",
        "first_name": "Larry", "last_name": "Landlord", "phone_number": "0712345601",
        "role": UserRole.LANDLORD, "kra_pin": "A123Z"
    }
    landlord = service.create_user(landlord_data)
    print(f"Created Landlord: {landlord.user_id}, KRA: {landlord.kra_pin}, Role: {landlord.role.value}")

    tenant_data = {
        "email": "tenant@example.com", "password": "securepassword", # testing password -> password_hash
        "first_name": "Terry", "last_name": "Tenant", "phone_number": "0712345602",
        "role": "TENANT", "kra_pin": "PIGNORE" # KRA should be ignored
    }
    tenant = service.create_user(tenant_data)
    print(f"Created Tenant: {tenant.user_id}, KRA: {tenant.kra_pin}, Role: {tenant.role.value}")
    print(f"Tenant password hash (should be 'securepassword'): {tenant.password_hash}")


    vendor_data = {
        "email": "vendor@example.com", "password_hash": "vendorpass",
        "first_name": "Wendy", "last_name": "Vendor", "phone_number": "0712345603",
        "role": UserRole.VENDOR, "vendor_services_offered": ["PLUMBING"]
    }
    vendor = service.create_user(vendor_data)
    print(f"Created Vendor: {vendor.user_id}, Services: {vendor.vendor_services_offered}")


    retrieved_landlord = service.get_user_by_email("landlord@example.com")
    if retrieved_landlord:
        print(f"Retrieved by email: {retrieved_landlord.first_name}")

    verified_user = service.verify_credentials("tenant@example.com", "securepassword")
    if verified_user:
        print(f"Verified tenant: {verified_user.first_name}")
    else:
        print("Tenant verification failed.")

    service.update_user(tenant.user_id, {"phone_number": "0799999999", "preferred_language": "SW_KE"})
    updated_tenant = service.get_user(tenant.user_id)
    if updated_tenant:
        print(f"Updated Tenant Phone: {updated_tenant.phone_number}, Lang: {updated_tenant.preferred_language.value}")

    service.delete_user(landlord.user_id)
    print(f"Users after deleting landlord: {[u.user_id for u in service.users]}")

    service.reset_password_for_user(tenant, "newpass123")
    print(f"Tenant new password hash: {tenant.password_hash}")

    service.update_vendor_average_rating_stats(vendor.user_id)
    updated_vendor = service.get_user(vendor.user_id)
    if updated_vendor:
        print(f"Vendor avg rating: {updated_vendor.vendor_rating_average}, total: {updated_vendor.vendor_total_ratings_count}")

    print("UserService stub testing complete.")
