import unittest
from datetime import datetime, date, timedelta
from decimal import Decimal
from services.lease_service import LeaseService
from models.lease import Lease, LeaseStatusType, LeaseSigningStatus # Assuming these are in models.lease
# Import User model if landlord_id or tenant_id needs to be validated against existing users
# from models.user import User
# Import Property model if property_id needs to be validated against existing properties
# from models.property import Property
from hermitta_app import create_app, db # Import app factory and db instance

class TestLeaseService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('test') # Use test configuration
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all() # Create all tables

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all() # Drop all tables
        cls.app_context.pop()

    def setUp(self):
        self.service = LeaseService()
        # It's good practice to also clear relevant tables before each test or ensure no cross-test interference.
        # For services that interact with multiple models, this might involve clearing those too.
        db.session.rollback() # Rollback any lingering transactions
        Lease.query.delete()
        # If User or Property models are created as part of lease tests by service, clear them:
        from models.user import User, UserRole # Import User for creating test users
        from models.property import Property, PropertyType # Import Property for creating test properties
        User.query.delete()
        Property.query.delete()
        db.session.commit()

        # Create prerequisite objects
        self.landlord = User(email="landlord_lease@example.com", phone_number="+254711111110", password_hash="test", first_name="Landlord", last_name="Lease", role=UserRole.LANDLORD)
        self.tenant = User(email="tenant_lease@example.com", phone_number="+254722222220", password_hash="test", first_name="Tenant", last_name="Lease", role=UserRole.TENANT)
        db.session.add_all([self.landlord, self.tenant])
        db.session.commit() # Commit to get IDs

        self.property = Property(landlord_id=self.landlord.user_id, address_line_1="1 Test St", city="Test City", county="Test County", property_type=PropertyType.APARTMENT_UNIT, num_bedrooms=1, num_bathrooms=1)
        db.session.add(self.property)
        db.session.commit() # Commit to get ID

        self.base_lease_data = {
            "property_id": self.property.property_id,
            "tenant_id": self.tenant.user_id,
            "landlord_id": self.landlord.user_id,
            "start_date": date(2024, 1, 1),
            "end_date": date(2024, 12, 31),
            "rent_amount": Decimal("1500.50"),
            "security_deposit": Decimal("3000.00"),
            "rent_due_day": 1,
            "status": LeaseStatusType.ACTIVE,
            "signing_status": LeaseSigningStatus.FULLY_SIGNED_SYSTEM,
            "move_in_date": date(2024, 1, 1),
            "lease_document_url": "http://example.com/lease.pdf",
            "notes": "Standard lease agreement."
        }
        self.required_lease_data = { # For tests that use string inputs for conversion
            # Note: These IDs will also need to exist for tests using this dict.
            # For simplicity, we might need another set of landlord/tenant/property for these,
            # or ensure these tests create their own prerequisites if IDs must be 2, 102.
            # For now, let's assume they will also use self.property.property_id etc.
            # or the tests using this dict will need specific setup.
            # To make it work immediately, I'll map them to the created ones.
            "property_id": self.property.property_id,
            "tenant_id": self.tenant.user_id,
            "landlord_id": self.landlord.user_id,
            "start_date": "2025-01-01",
            "end_date": "2025-12-31",
            "rent_amount": "2000",
            "security_deposit": "4000.00",
            "rent_due_day": 1,
            "move_in_date": "2025-01-01",
        }

    def tearDown(self):
        db.session.rollback()
        Lease.query.delete()
        from models.user import User # Import User for cleanup
        from models.property import Property # Import Property for cleanup
        User.query.delete()
        Property.query.delete()
        db.session.commit()


    def test_create_lease_success(self):
        lease_data = self.base_lease_data.copy()
        created_lease = self.service.create_lease(lease_data)

        self.assertIsInstance(created_lease, Lease)
        self.assertIsNotNone(created_lease.lease_id) # Should be set by DB
        self.assertEqual(created_lease.property_id, lease_data["property_id"])
        self.assertEqual(created_lease.start_date, lease_data["start_date"])
        self.assertEqual(created_lease.rent_amount, lease_data["rent_amount"])
        self.assertEqual(created_lease.status, lease_data["status"])
        self.assertEqual(created_lease.signing_status, lease_data["signing_status"])
        self.assertIsInstance(created_lease.created_at, datetime)
        self.assertIsInstance(created_lease.updated_at, datetime)
        # self.assertEqual(len(self.service.leases), 1) # Service might not maintain an in-memory list
        # self.assertEqual(self.service.leases[0], created_lease)

    def test_create_lease_with_string_enums_and_types(self):
        data = self.required_lease_data.copy()
        data["status"] = "DRAFT"
        data["signing_status"] = "SENT_FOR_SIGNATURE"
        data["move_in_date"] = "2025-01-05"

        created_lease = self.service.create_lease(data)
        self.assertIsInstance(created_lease, Lease)
        self.assertEqual(created_lease.property_id, data["property_id"])
        self.assertEqual(created_lease.start_date, date(2025, 1, 1)) # Assuming service converts string
        self.assertEqual(created_lease.end_date, date(2025, 12, 31)) # Assuming service converts string
        self.assertEqual(created_lease.move_in_date, date(2025, 1, 5)) # Assuming service converts string
        self.assertEqual(created_lease.rent_amount, Decimal("2000")) # Assuming service converts string
        self.assertEqual(created_lease.security_deposit, Decimal("4000.00")) # Assuming service converts string
        self.assertEqual(created_lease.status, LeaseStatusType.DRAFT) # Assuming service converts string to enum
        self.assertEqual(created_lease.signing_status, LeaseSigningStatus.SENT_FOR_SIGNATURE) # Assuming service converts

    def test_create_lease_defaults_statuses_if_not_provided(self):
        data_defaults = self.required_lease_data.copy()
        # Ensure 'status' and 'signing_status' are not in data_defaults if they are to be defaulted by service
        if 'status' in data_defaults: del data_defaults['status']
        if 'signing_status' in data_defaults: del data_defaults['signing_status']

        created_lease = self.service.create_lease(data_defaults)
        self.assertEqual(created_lease.status, LeaseStatusType.DRAFT) # Assuming service sets this default
        self.assertEqual(created_lease.signing_status, LeaseSigningStatus.NOT_STARTED) # Assuming service sets this

    def test_create_lease_missing_required_fields(self):
        # This test relies on the service layer performing validation before model instantiation
        # or catching TypeErrors from the model and re-raising as ValueError.
        # The exact missing fields message depends on the service's validation logic.
        # For example, if 'property_id' is missing:
        incomplete_data_no_prop = {k: v for k, v in self.required_lease_data.items() if k != 'property_id'}
        with self.assertRaisesRegex(ValueError, r"Missing required fields.*property_id"):
             self.service.create_lease(incomplete_data_no_prop)

        # Example: Missing 'start_date'
        incomplete_data_no_start = {k: v for k, v in self.required_lease_data.items() if k != 'start_date'}
        with self.assertRaisesRegex(ValueError, r"Missing required fields.*start_date"):
             self.service.create_lease(incomplete_data_no_start)


    def test_create_lease_invalid_enum_string(self):
        data = self.required_lease_data.copy()
        data["status"] = "NON_EXISTENT_STATUS" # Invalid enum string
        with self.assertRaisesRegex(ValueError, "Invalid status string: NON_EXISTENT_STATUS"): # Or more general error from service
            self.service.create_lease(data)

    def test_create_lease_invalid_date_string(self):
        data = self.required_lease_data.copy()
        data["start_date"] = "01/01/2024" # Invalid date format for service's expected parser
        with self.assertRaisesRegex(ValueError, "Invalid date string for 'start_date'"):
            self.service.create_lease(data)

    def test_create_lease_invalid_decimal_string(self):
        data = self.required_lease_data.copy()
        data["rent_amount"] = "one thousand" # Invalid decimal string
        with self.assertRaisesRegex(ValueError, "Invalid value for Decimal field 'rent_amount'"):
            self.service.create_lease(data)

    def test_get_lease_found(self):
        created_lease = self.service.create_lease(self.base_lease_data.copy())
        found_lease = self.service.get_lease_by_id(created_lease.lease_id) # Renamed for clarity
        self.assertIsNotNone(found_lease)
        self.assertEqual(found_lease.lease_id, created_lease.lease_id)

    def test_get_lease_not_found(self):
        found_lease = self.service.get_lease_by_id(99999) # Use a clearly non-existent ID
        self.assertIsNone(found_lease)

    def test_update_lease_success(self):
        created_lease = self.service.create_lease(self.base_lease_data.copy())
        original_updated_at = created_lease.updated_at

        update_data = {
            "notes": "Updated lease terms.",
            "rent_amount": "1550.75",
            "status": "EXPIRED"
        }

        updated_lease = self.service.update_lease(created_lease.lease_id, update_data)

        self.assertIsNotNone(updated_lease)
        self.assertEqual(updated_lease.notes, "Updated lease terms.")
        self.assertEqual(updated_lease.rent_amount, Decimal("1550.75")) # Assuming service converts
        self.assertEqual(updated_lease.status, LeaseStatusType.EXPIRED) # Assuming service converts
        self.assertTrue(updated_lease.updated_at > original_updated_at)

        refetched_lease = self.service.get_lease_by_id(created_lease.lease_id)
        self.assertEqual(refetched_lease.notes, "Updated lease terms.")
        self.assertEqual(refetched_lease.updated_at, updated_lease.updated_at)

    def test_update_lease_not_found(self):
        update_data = {"notes": "This should not apply."}
        updated_lease = self.service.update_lease(99999, update_data)
        self.assertIsNone(updated_lease)

    def test_delete_lease_success(self):
        created_lease = self.service.create_lease(self.base_lease_data.copy())
        # self.assertEqual(len(self.service.leases), 1) # Service might not maintain an in-memory list

        delete_result = self.service.delete_lease(created_lease.lease_id)
        self.assertTrue(delete_result)
        # self.assertEqual(len(self.service.leases), 0)

        not_found_lease = self.service.get_lease_by_id(created_lease.lease_id)
        self.assertIsNone(not_found_lease)

    def test_delete_lease_not_found(self):
        delete_result = self.service.delete_lease(99999)
        self.assertFalse(delete_result)

if __name__ == '__main__':
    unittest.main()
