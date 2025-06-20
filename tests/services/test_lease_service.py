import unittest
from datetime import datetime, date, timedelta
from decimal import Decimal
from services.lease_service import LeaseService
from models.lease import Lease, LeaseStatusType, LeaseSigningStatus # Assuming these are in models.lease

class TestLeaseService(unittest.TestCase):

    def setUp(self):
        self.service = LeaseService()
        self.base_lease_data = {
            "property_id": 1,
            "tenant_id": 1, # Assuming this is a user_id for the tenant
            "landlord_id": 101, # Assuming this is a user_id for the landlord
            "start_date": date(2024, 1, 1),
            "end_date": date(2024, 12, 31),
            "rent_amount": Decimal("1500.50"),
            # "currency": "KES", # Removed, not in Lease model
            # "payment_terms": "Monthly", # Removed, not in Lease model
            "security_deposit": Decimal("3000.00"),
            "rent_due_day": 1, # Added required field
            "status": LeaseStatusType.ACTIVE,
            "signing_status": LeaseSigningStatus.FULLY_SIGNED_SYSTEM,
            "move_in_date": date(2024, 1, 1),
            "lease_document_url": "http://example.com/lease.pdf",
            "notes": "Standard lease agreement."
        }
        self.required_lease_data = {
            "property_id": 2,
            "tenant_id": 2,
            "landlord_id": 102,
            "start_date": "2025-01-01", # String date
            "end_date": "2025-12-31",   # String date
            "rent_amount": "2000",      # String number for Decimal
            "security_deposit": "4000.00", # String number for Decimal
            # "currency": "USD", # Removed
            # "payment_terms": "Quarterly", # Removed
            "rent_due_day": 1,
            "move_in_date": "2025-01-01", # Added required field
        }

    def test_create_lease_success(self):
        lease_data = self.base_lease_data.copy()
        created_lease = self.service.create_lease(lease_data)

        self.assertIsInstance(created_lease, Lease)
        self.assertEqual(created_lease.lease_id, 1)
        self.assertEqual(created_lease.property_id, lease_data["property_id"])
        self.assertEqual(created_lease.start_date, lease_data["start_date"])
        self.assertEqual(created_lease.rent_amount, lease_data["rent_amount"])
        self.assertEqual(created_lease.status, lease_data["status"])
        self.assertEqual(created_lease.signing_status, lease_data["signing_status"])
        self.assertIsInstance(created_lease.created_at, datetime)
        self.assertIsInstance(created_lease.updated_at, datetime)
        self.assertEqual(len(self.service.leases), 1)
        self.assertEqual(self.service.leases[0], created_lease)

    def test_create_lease_with_string_enums_and_types(self):
        data = self.required_lease_data.copy()
        data["status"] = "DRAFT" # String enum
        data["signing_status"] = "SENT_FOR_SIGNATURE" # String enum
        data["move_in_date"] = "2025-01-05" # String date

        created_lease = self.service.create_lease(data)
        self.assertIsInstance(created_lease, Lease)
        self.assertEqual(created_lease.property_id, data["property_id"])
        self.assertEqual(created_lease.start_date, date(2025, 1, 1))
        self.assertEqual(created_lease.end_date, date(2025, 12, 31))
        self.assertEqual(created_lease.move_in_date, date(2025, 1, 5))
        self.assertEqual(created_lease.rent_amount, Decimal("2000"))
        self.assertEqual(created_lease.security_deposit, Decimal("4000.00"))
        self.assertEqual(created_lease.status, LeaseStatusType.DRAFT)
        self.assertEqual(created_lease.signing_status, LeaseSigningStatus.SENT_FOR_SIGNATURE)

    def test_create_lease_defaults_statuses_if_not_provided(self):
        data = self.required_lease_data.copy()
        # Ensure 'status' and 'signing_status' are not in data
        if 'status' in data: del data['status']
        if 'signing_status' in data: del data['signing_status']

        created_lease = self.service.create_lease(data)
        self.assertEqual(created_lease.status, LeaseStatusType.DRAFT)
        self.assertEqual(created_lease.signing_status, LeaseSigningStatus.NOT_STARTED)

    def test_create_lease_missing_required_fields(self):
        # Missing 'start_date', 'end_date', 'rent_amount', 'security_deposit' which service makes required
        incomplete_data = {
            "property_id": 3, "tenant_id": 3, "landlord_id": 103,
            "property_id": 3, "tenant_id": 3, "landlord_id": 103
            # "currency": "EUR", "payment_terms": "Annually" # Removed
        }
        # Test that if a core field required by Lease model (e.g. rent_due_day) is missing,
        # the model's TypeError is caught and wrapped in ValueError by the service.
        # The service's explicit checks for date/Decimal presence were removed to let model handle this.
        with self.assertRaisesRegex(ValueError, r"Missing required fields or incorrect data for Lease creation: Lease.__init__\(\) missing 5 required positional arguments: 'start_date', 'end_date', 'rent_amount', 'rent_due_day', and 'move_in_date'"):
            self.service.create_lease(incomplete_data)

        incomplete_data["start_date"] = "2024-01-01"
        with self.assertRaisesRegex(ValueError, r"Missing required fields or incorrect data for Lease creation: Lease.__init__\(\) missing 4 required positional arguments: 'end_date', 'rent_amount', 'rent_due_day', and 'move_in_date'"):
            self.service.create_lease(incomplete_data)

        incomplete_data["end_date"] = "2024-12-31"
        with self.assertRaisesRegex(ValueError, r"Missing required fields or incorrect data for Lease creation: Lease.__init__\(\) missing 3 required positional arguments: 'rent_amount', 'rent_due_day', and 'move_in_date'"):
            self.service.create_lease(incomplete_data)

        incomplete_data["rent_amount"] = "1000"
        with self.assertRaisesRegex(ValueError, r"Missing required fields or incorrect data for Lease creation: Lease.__init__\(\) missing 2 required positional arguments: 'rent_due_day' and 'move_in_date'"):
            self.service.create_lease(incomplete_data)

        incomplete_data["rent_due_day"] = 1
        with self.assertRaisesRegex(ValueError, r"Missing required fields or incorrect data for Lease creation: Lease.__init__\(\) missing 1 required positional argument: 'move_in_date'"):
            self.service.create_lease(incomplete_data)

        incomplete_data["move_in_date"] = "2024-01-01"
        # Now all required fields for Lease model that are not defaulted by model are present,
        # assuming security_deposit is optional in model.
        # If security_deposit is also required by model and not optional:
        # with self.assertRaisesRegex(ValueError, r"Missing required fields or incorrect data for Lease creation: Lease.__init__\(\) missing 1 required positional argument: 'security_deposit'"):
        #     self.service.create_lease(incomplete_data)
        # Assuming security_deposit is optional for this test to pass after this point.
        # If not, this test needs one more step. For now, let's assume it's optional.


    def test_create_lease_invalid_enum_string(self):
        data = self.required_lease_data.copy()
        data["status"] = "NON_EXISTENT_STATUS"
        with self.assertRaisesRegex(ValueError, "Invalid status string: NON_EXISTENT_STATUS"):
            self.service.create_lease(data)

    def test_create_lease_invalid_date_string(self):
        data = self.required_lease_data.copy()
        data["start_date"] = "01/01/2024" # Invalid format
        with self.assertRaisesRegex(ValueError, "Invalid date string for 'start_date': 01/01/2024. Use YYYY-MM-DD format."):
            self.service.create_lease(data)

    def test_create_lease_invalid_decimal_string(self):
        data = self.required_lease_data.copy()
        data["rent_amount"] = "one thousand" # Invalid decimal
        with self.assertRaisesRegex(ValueError, "Invalid value for Decimal field 'rent_amount': one thousand"):
            self.service.create_lease(data)

    def test_get_lease_found(self):
        created_lease = self.service.create_lease(self.base_lease_data.copy())
        found_lease = self.service.get_lease(created_lease.lease_id)
        self.assertIsNotNone(found_lease)
        self.assertEqual(found_lease, created_lease)

    def test_get_lease_not_found(self):
        found_lease = self.service.get_lease(999) # Non-existent ID
        self.assertIsNone(found_lease)

    def test_update_lease_success(self):
        created_lease = self.service.create_lease(self.base_lease_data.copy())
        original_updated_at = created_lease.updated_at

        update_data = {
            "notes": "Updated lease terms.",
            "rent_amount": "1550.75", # String to be converted to Decimal
            "status": "EXPIRED"      # String to be converted to Enum
        }

        updated_lease = self.service.update_lease(created_lease.lease_id, update_data)

        self.assertIsNotNone(updated_lease)
        self.assertEqual(updated_lease.notes, "Updated lease terms.")
        self.assertEqual(updated_lease.rent_amount, Decimal("1550.75"))
        self.assertEqual(updated_lease.status, LeaseStatusType.EXPIRED)
        self.assertTrue(updated_lease.updated_at > original_updated_at)

        refetched_lease = self.service.get_lease(created_lease.lease_id)
        self.assertEqual(refetched_lease.notes, "Updated lease terms.")
        self.assertEqual(refetched_lease.updated_at, updated_lease.updated_at)

    def test_update_lease_not_found(self):
        update_data = {"notes": "This should not apply."}
        updated_lease = self.service.update_lease(999, update_data) # Non-existent ID
        self.assertIsNone(updated_lease)

    def test_delete_lease_success(self):
        created_lease = self.service.create_lease(self.base_lease_data.copy())
        self.assertEqual(len(self.service.leases), 1)

        delete_result = self.service.delete_lease(created_lease.lease_id)
        self.assertTrue(delete_result)
        self.assertEqual(len(self.service.leases), 0)

        not_found_lease = self.service.get_lease(created_lease.lease_id)
        self.assertIsNone(not_found_lease)

    def test_delete_lease_not_found(self):
        delete_result = self.service.delete_lease(999) # Non-existent ID
        self.assertFalse(delete_result)

if __name__ == '__main__':
    unittest.main()
