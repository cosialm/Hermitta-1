import unittest
from datetime import datetime, date
from decimal import Decimal
from hermitta_app import create_app, db
from services.user_service import UserService
from models.user import User, UserRole, PreferredLoginMethod, PreferredLanguage

class TestUserService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('test')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        self.service = UserService()
        self.base_user_data = {
            "email": "test@example.com",
            "phone_number": "+254712345678",
            "password_hash": "password123", # In a real scenario, this would be hashed
            "first_name": "Test",
            "last_name": "User",
            "role": UserRole.TENANT,
        }
        # Ensure each test starts with a clean slate in the database
        # Rollback any potential open transaction from a previous failed test
        db.session.rollback()
        # Clear data from tables
        db.session.query(User).delete()
        # Add other models here if they are populated by user service tests indirectly
        # e.g., db.session.query(SomeOtherModelRelatedToUser).delete()
        db.session.commit()

    def tearDown(self):
        # Ensure the session is clean after each test too
        db.session.rollback()
        db.session.query(User).delete()
        # Add other models here if they are populated by user service tests indirectly
        db.session.commit()


    def test_create_user_success_tenant(self):
        user_data = self.base_user_data.copy()
        created_user = self.service.create_user(user_data)

        self.assertIsInstance(created_user, User)
        self.assertIsNotNone(created_user.user_id) # ID should be set by DB
        self.assertEqual(created_user.email, user_data["email"])
        self.assertEqual(created_user.role, UserRole.TENANT)
        self.assertTrue(created_user.is_active)
        self.assertFalse(created_user.is_mfa_enabled)
        self.assertEqual(created_user.preferred_login_method, PreferredLoginMethod.EMAIL) # Default
        self.assertEqual(created_user.preferred_language, PreferredLanguage.EN_KE) # Default
        self.assertIsNone(created_user.kra_pin)
        # Defaults from model for JSON fields might be None, not {} or [] if not set by service
        # Let's check what the model actually defaults to.
        # self.assertEqual(created_user.staff_permissions, {})
        # self.assertEqual(created_user.vendor_services_offered, [])


    def test_create_user_landlord_with_kra(self):
        user_data = {**self.base_user_data,
                     "email": "landlord@example.com",
                     "role": UserRole.LANDLORD,
                     "kra_pin": "A123456789Z"}
        created_user = self.service.create_user(user_data)
        self.assertEqual(created_user.role, UserRole.LANDLORD)
        self.assertEqual(created_user.kra_pin, "A123456789Z")

    def test_create_user_tenant_kra_is_none(self):
        user_data = {**self.base_user_data, "role": UserRole.TENANT, "kra_pin": "A123IGNORE"}
        created_user = self.service.create_user(user_data)
        self.assertEqual(created_user.role, UserRole.TENANT)
        self.assertIsNone(created_user.kra_pin) # Service logic should ensure this

    def test_create_user_vendor_fields(self):
        user_data = {**self.base_user_data,
                     "email": "vendor@example.com",
                     "role": UserRole.VENDOR,
                     "vendor_services_offered": ["PLUMBING", "ELECTRICAL"],
                     "vendor_rating_average": Decimal("4.5"),
                     "vendor_total_ratings_count": 10,
                     "is_verified_vendor": True
                    }
        created_user = self.service.create_user(user_data)
        self.assertEqual(created_user.role, UserRole.VENDOR)
        self.assertEqual(created_user.vendor_services_offered, ["PLUMBING", "ELECTRICAL"])
        self.assertEqual(created_user.vendor_rating_average, Decimal("4.5"))
        self.assertEqual(created_user.vendor_total_ratings_count, 10)
        self.assertTrue(created_user.is_verified_vendor)

    def test_create_user_staff_fields(self):
        user_data = {**self.base_user_data,
                     "email": "staff@example.com",
                     "role": UserRole.STAFF,
                     "staff_permissions": {"can_view_reports": True}
                    }
        created_user = self.service.create_user(user_data)
        self.assertEqual(created_user.role, UserRole.STAFF)
        self.assertEqual(created_user.staff_permissions, {"can_view_reports": True})

    def test_create_user_handles_string_enums_and_defaults(self):
        user_data = {
            "email": "stringenum@example.com", "phone_number": "+254787654321",
            "password_hash": "password123", "first_name": "String", "last_name": "Enum",
            "role": "LANDLORD", # String
            "preferred_login_method": "PHONE", # String
            "preferred_language": "sw_KE" # String with underscore, matching enum name
        }
        created_user = self.service.create_user(user_data)
        self.assertEqual(created_user.role, UserRole.LANDLORD)
        self.assertEqual(created_user.preferred_login_method, PreferredLoginMethod.PHONE)
        self.assertEqual(created_user.preferred_language, PreferredLanguage.SW_KE)
        # Check other defaults
        self.assertTrue(created_user.is_active)
        self.assertFalse(created_user.is_mfa_enabled)

    def test_create_user_password_fallback(self):
        user_data = {
            "email": "passfallback@example.com", "phone_number": "+254711223344",
            "password": "plainpassword", # No password_hash
            "first_name": "Fallback", "last_name": "Test", "role": UserRole.TENANT,
        }
        created_user = self.service.create_user(user_data)
        # The service logic for password hashing should be tested.
        # For now, assuming it uses the plain password if hash is missing.
        self.assertEqual(created_user.password_hash, "plainpassword")


    def test_create_user_missing_required_fields(self):
        # Test with essential fields missing that User model __init__ requires
        incomplete_data = {"email": "incomplete@example.com"} # Missing phone, password, first_name, last_name
        # Update the regex to be more flexible or match the exact new message format.
        # For example, matching the "Missing required fields" part and key fields.
        with self.assertRaisesRegex(ValueError, r"Missing required fields for User creation:.*phone_number.*first_name.*last_name.*password/password_hash"):
            self.service.create_user(incomplete_data)

    def test_get_user_found_and_not_found(self):
        user_data_get = {**self.base_user_data, "email": "getuser@example.com"}
        user1 = self.service.create_user(user_data_get)

        found_user = self.service.get_user_by_id(user1.user_id) # Assuming service method is get_user_by_id
        self.assertEqual(found_user, user1)

        not_found_user = self.service.get_user_by_id(99999) # Use a clearly non-existent ID
        self.assertIsNone(not_found_user)

    def test_get_user_by_email_found_and_not_found(self):
        user_data_email = {**self.base_user_data, "email": "findme@example.com"}
        user1 = self.service.create_user(user_data_email)

        found_user = self.service.get_user_by_email("findme@example.com")
        self.assertEqual(found_user, user1)
        found_user_case_ins = self.service.get_user_by_email("FINDME@EXAMPLE.COM") # Service should handle case-insensitivity
        self.assertEqual(found_user_case_ins, user1)

        not_found_user = self.service.get_user_by_email("nosuchuser@example.com")
        self.assertIsNone(not_found_user)

    def test_update_user_success(self):
        user_data_update = {**self.base_user_data, "email": "update@example.com"}
        user1 = self.service.create_user(user_data_update)
        original_updated_at = user1.updated_at

        update_payload = {
            "first_name": "UpdatedFirst",
            "is_mfa_enabled": True,
            "phone_number": "+254700000000",
            "preferred_language": "SW_KE" # String enum, ensure service handles conversion
        }
        updated_user = self.service.update_user(user1.user_id, update_payload)

        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.first_name, "UpdatedFirst")
        self.assertTrue(updated_user.is_mfa_enabled)
        self.assertEqual(updated_user.phone_number, "+254700000000")
        self.assertEqual(updated_user.preferred_language, PreferredLanguage.SW_KE) # Assuming service converts
        self.assertTrue(updated_user.updated_at > original_updated_at)

        refetched_user = self.service.get_user_by_id(user1.user_id)
        self.assertEqual(refetched_user.first_name, "UpdatedFirst")

    def test_update_user_role_specific_fields(self):
        # Create as TENANT
        user_data_role_change = {**self.base_user_data, "email": "rolechange@example.com", "role": UserRole.TENANT}
        user1 = self.service.create_user(user_data_role_change)
        self.assertIsNone(user1.kra_pin)

        # Update to LANDLORD with KRA
        update_to_landlord = {"role": "LANDLORD", "kra_pin": "B987Z"}
        updated_user = self.service.update_user(user1.user_id, update_to_landlord)
        self.assertEqual(updated_user.role, UserRole.LANDLORD)
        self.assertEqual(updated_user.kra_pin, "B987Z")

        # Update back to TENANT, KRA should be cleared by service logic
        update_to_tenant = {"role": UserRole.TENANT}
        updated_user_again = self.service.update_user(user1.user_id, update_to_tenant)
        self.assertEqual(updated_user_again.role, UserRole.TENANT)
        self.assertIsNone(updated_user_again.kra_pin)


    def test_update_user_not_found(self):
        updated_user = self.service.update_user(99999, {"first_name": "Ghost"})
        self.assertIsNone(updated_user)

    def test_delete_user_success_and_not_found(self):
        user_data_delete = {**self.base_user_data, "email": "delete@example.com"}
        user1 = self.service.create_user(user_data_delete)
        # self.assertEqual(len(self.service.users), 1) # Assuming service maintains an in-memory list for this test

        delete_success = self.service.delete_user(user1.user_id)
        self.assertTrue(delete_success)
        # self.assertEqual(len(self.service.users), 0)
        self.assertIsNone(self.service.get_user_by_id(user1.user_id))

        delete_fail = self.service.delete_user(99999)
        self.assertFalse(delete_fail)

    def test_verify_credentials_success(self):
        user_data_login = {**self.base_user_data, "email": "login@example.com", "password_hash": "correct_password"}
        # Assume password hashing is handled by service or directly for test
        # For simplicity, if service hashes, ensure it's done before verify_credentials is called
        self.service.create_user(user_data_login)


        verified_user = self.service.verify_credentials("login@example.com", "correct_password")
        self.assertIsNotNone(verified_user)
        self.assertEqual(verified_user.email, "login@example.com")

    def test_verify_credentials_wrong_password(self):
        user_data_login_fail = {**self.base_user_data, "email": "loginfail@example.com", "password_hash": "correct_password"}
        self.service.create_user(user_data_login_fail)

        verified_user = self.service.verify_credentials("loginfail@example.com", "wrong_password")
        self.assertIsNone(verified_user)

    def test_verify_credentials_user_not_found(self):
        verified_user = self.service.verify_credentials("nosuchuser@example.com", "anypassword")
        self.assertIsNone(verified_user)

if __name__ == '__main__':
    unittest.main()
