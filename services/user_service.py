from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal
from hermitta_app import db # Import db instance
from models.user import User, UserRole, PreferredLoginMethod, PreferredLanguage # Import SQLAlchemy model

# TODO: Implement actual password hashing and verification (e.g., using werkzeug.security)
# For now, password_hash is treated as a plain string.

class UserService:
    def _prepare_user_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepares user data for creation or update, handling enums and specific logic.
        """
        prepared_data = user_data.copy()

        # Convert string enums to Enum members
        if 'role' in prepared_data and isinstance(prepared_data['role'], str):
            prepared_data['role'] = UserRole[prepared_data['role'].upper()]
        if 'preferred_login_method' in prepared_data and isinstance(prepared_data['preferred_login_method'], str):
            prepared_data['preferred_login_method'] = PreferredLoginMethod[prepared_data['preferred_login_method'].upper()]
        if 'preferred_language' in prepared_data and isinstance(prepared_data['preferred_language'], str):
            prepared_data['preferred_language'] = PreferredLanguage[prepared_data['preferred_language'].upper()]

        # KRA PIN logic: Only set if role is LANDLORD
        if 'role' in prepared_data and prepared_data['role'] != UserRole.LANDLORD:
            prepared_data['kra_pin'] = None
        elif 'role' not in prepared_data and 'kra_pin' in prepared_data: # if role not changing but KRA pin provided
            # This case needs context of existing user's role if it's an update.
            # For simplicity, service methods should handle this explicitly.
            pass


        # Vendor specific fields: clear if not VENDOR role
        if 'role' in prepared_data and prepared_data['role'] != UserRole.VENDOR:
            prepared_data['vendor_services_offered'] = None # Or [] if model expects list
            prepared_data['vendor_rating_average'] = None
            prepared_data['vendor_total_ratings_count'] = None
            prepared_data['is_verified_vendor'] = None

        if 'vendor_rating_average' in prepared_data and prepared_data['vendor_rating_average'] is not None:
            prepared_data['vendor_rating_average'] = Decimal(str(prepared_data['vendor_rating_average']))

        # Password: if 'password' is provided, it should be hashed and stored in 'password_hash'
        # This service assumes 'password_hash' is provided directly if 'password' isn't.
        if 'password' in prepared_data:
            # In a real app: prepared_data['password_hash'] = generate_password_hash(prepared_data.pop('password'))
            prepared_data['password_hash'] = prepared_data.pop('password') # STUB: using plain password as hash

        return prepared_data

    def create_user(self, user_data: Dict[str, Any]) -> User:
        """
        Creates a new user.
        user_data should contain all necessary fields.
        Password should be provided as 'password' (to be hashed) or 'password_hash' (pre-hashed).
        """
        required_fields = ['email', 'phone_number', 'first_name', 'last_name']
        # Password check is special: either 'password' or 'password_hash' must be present
        has_password = 'password' in user_data or 'password_hash' in user_data

        missing_fields = [field for field in required_fields if field not in user_data]
        if not has_password:
            missing_fields.append("password/password_hash")

        if missing_fields:
            raise ValueError(f"Missing required fields for User creation: {', '.join(missing_fields)}")

        prepared_data = self._prepare_user_data(user_data)

        # Ensure KRA PIN is None if role is not LANDLORD (already handled in _prepare_user_data but good for explicitness)
        if prepared_data.get('role') != UserRole.LANDLORD:
            prepared_data['kra_pin'] = None

        try:
            new_user = User(**prepared_data)
            db.session.add(new_user)
            db.session.commit()
        except Exception as e: # Catch potential DB errors or other issues during User instantiation
            db.session.rollback()
            # It might be better to let specific SQLAlchemy errors propagate if they are distinct
            # from validation errors, or wrap them in a custom service exception.
            raise ValueError(f"Error during User creation: {e}")
        return new_user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return User.query.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return User.query.filter(User.email.ilike(email)).first()

    def get_user_by_phone_number(self, phone_number: str) -> Optional[User]:
        return User.query.filter_by(phone_number=phone_number).first()

    def update_user(self, user_id: int, update_data: Dict[str, Any]) -> Optional[User]:
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        prepared_data = self._prepare_user_data(update_data)

        # Determine the role after update for KRA PIN logic
        final_role = prepared_data.get('role', user.role)

        for key, value in prepared_data.items():
            if key == 'kra_pin':
                if final_role == UserRole.LANDLORD:
                    setattr(user, key, value)
                else:
                    # If role is not LANDLORD (or changing to non-LANDLORD), KRA PIN should be None
                    user.kra_pin = None
            elif hasattr(user, key):
                setattr(user, key, value)

        # If role itself was updated and new role is not LANDLORD, ensure kra_pin is None
        if 'role' in prepared_data and prepared_data['role'] != UserRole.LANDLORD:
            user.kra_pin = None
        # If role was not updated, but user is not LANDLORD, and kra_pin was in update_data,
        # it would have been set to None by the loop logic above if final_role was not LANDLORD.

        db.session.commit()
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    def verify_credentials(self, email: str, password_to_check: str) -> Optional[User]:
        user = self.get_user_by_email(email)
        if user:
            # STUB: Direct comparison. Real service uses e.g. check_password_hash(user.password_hash, password_to_check)
            if user.password_hash == password_to_check:
                return user
        return None

    def reset_password(self, user_id: int, new_password: str) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            # STUB: Real app: user.password_hash = generate_password_hash(new_password)
            user.password_hash = new_password
            db.session.commit()
            return True
        return False

    # --- Dummy/Placeholder methods from original service for potential test compatibility ---
    # These might need to be re-evaluated or removed if not used by actual client code (routes)

    def get_user_by_token(self, token: str) -> Optional[User]: # Used in auth_routes tests
        # Dummy: in real app, token is validated and user fetched.
        # For stub, assume token is user_id as string.
        try:
            user_id = int(token) # This is not a secure way to handle tokens
            return self.get_user_by_id(user_id)
        except ValueError:
            return None

    def get_current_landlord_id(self) -> Optional[int]: # Dummy
        # This would depend on auth context, e.g. current_user from Flask-Login
        # For now, return a dummy ID or None
        return 1

    def get_current_tenant_user(self) -> Optional[User]: # Dummy
        # Placeholder: Get user 1 and assume it's a tenant
        user = self.get_user_by_id(1)
        return user if user and user.role == UserRole.TENANT else None

    def get_current_user_with_roles(self) -> Optional[User]: # Dummy
        return self.get_user_by_id(1) # Placeholder

    def get_current_authenticated_user_id(self) -> Optional[int]: # Dummy
        return 1 # Placeholder

    def ensure_landlord_permission_for_property(self, landlord_id: int, property_id: int) -> bool: # Dummy
        # Real logic: check if property.landlord_id == landlord_id
        return True

    def ensure_admin_role(self) -> bool: # Dummy
        # Real logic: check current_user.role == UserRole.ADMIN
        return True

    def get_vendor_details_for_rating_list(self, vendor_id: int) -> Optional[User]:
        user = self.get_user_by_id(vendor_id)
        return user if user and user.role == UserRole.VENDOR else None

    def update_vendor_average_rating_stats(self, vendor_id: int) -> bool:
        user = self.get_user_by_id(vendor_id)
        if user and user.role == UserRole.VENDOR:
            # Dummy logic, real logic would fetch all ratings and calculate
            # For example, from a VendorPerformanceRating model
            user.vendor_rating_average = Decimal("4.5") # Dummy value
            user.vendor_total_ratings_count = (user.vendor_total_ratings_count or 0) + 1 # Dummy increment
            db.session.commit()
            return True
        return False

    def validate_vendor_ids(self, vendor_ids: List[int]) -> bool: # Dummy
        # Real logic: check if all vendor_ids exist and are vendors
        return True

    def get_current_vendor_user_id(self) -> Optional[int]: # Dummy
        # Placeholder: Assume user 1 is a vendor
        user = self.get_user_by_id(1)
        return user.user_id if user and user.role == UserRole.VENDOR else None

# Example Usage (would be done in a Flask context with app and db initialized)
# if __name__ == '__main__':
#     # This example usage would require a Flask app context to use db.session
#     # from hermitta_app import create_app
#     # app = create_app('dev')
#     # with app.app_context():
#     #     service = UserService()
#     #     landlord_data = {
#     #         "email": "landlord.sqlalchemy@example.com", "password": "pass123",
#     #         "first_name": "LarrySQL", "last_name": "Landlord", "phone_number": "0712345611",
#     #         "role": UserRole.LANDLORD, "kra_pin": "A999Z"
#     #     }
#     #     landlord = service.create_user(landlord_data)
#     #     print(f"Created Landlord: {landlord.user_id}, Email: {landlord.email}, KRA: {landlord.kra_pin}")

#     #     tenant_data = {
#     #         "email": "tenant.sqlalchemy@example.com", "password": "securepassword",
#     #         "first_name": "TerrySQL", "last_name": "Tenant", "phone_number": "0712345612",
#     #         "role": UserRole.TENANT
#     #     }
#     #     tenant = service.create_user(tenant_data)
#     #     print(f"Created Tenant: {tenant.user_id}, Email: {tenant.email}, KRA: {tenant.kra_pin}")

#     #     retrieved_user = service.get_user_by_email("landlord.sqlalchemy@example.com")
#     #     if retrieved_user:
#     #         print(f"Retrieved by email: {retrieved_user.first_name}")

#     #     verified = service.verify_credentials("tenant.sqlalchemy@example.com", "securepassword")
#     #     if verified:
#     #         print(f"Verified tenant: {verified.first_name}")

#     #     service.update_user(tenant.user_id, {"phone_number": "0799999988", "preferred_language": UserRole.SW_KE})
#     #     updated_tenant = service.get_user_by_id(tenant.user_id)
#     #     if updated_tenant:
#     #         print(f"Updated Tenant Phone: {updated_tenant.phone_number}, Lang: {updated_tenant.preferred_language.value}")

#     #     # service.delete_user(landlord.user_id)
#     #     # print(f"Landlord deleted status: {service.get_user_by_id(landlord.user_id) is None}")
#     #     print("UserService SQLAlchemy testing placeholders complete.")
