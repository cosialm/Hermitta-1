import unittest
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List, Dict # Added for type hinting if needed later

# Assuming the Lease model and its enums are in models.lease
# This import will be problematic if models.lease doesn't exist or
# if the test isn't run in an environment where 'models' is discoverable.
from models.lease import Lease, LeaseStatusType, LeaseSigningStatus

class TestLeaseModel(unittest.TestCase):

    def setUp(self):
        """Common data for lease instantiation if needed."""
        self.common_lease_data = {
            "lease_id": 1,
            "property_id": 101,
            "landlord_id": 201,
            "tenant_id": 301, # Assuming tenant_id is optional but provided for some tests
            "start_date": date(2024, 1, 1),
            "end_date": date(2024, 12, 31),
            "rent_amount": Decimal("1200.00"),
            "rent_due_day": 1,
            "move_in_date": date(2024, 1, 1),
            "security_deposit": Decimal("1000.00"),
            # created_at and updated_at are typically set by the model/ORM
        }

    def test_lease_creation_basic(self):
        """Test basic Lease instantiation with required fields and default statuses."""
        lease_data = self.common_lease_data.copy()

        # For this test, explicitly remove fields that have defaults to test those defaults
        # or are optional and not being tested here.
        # Keep required ones: lease_id, property_id, landlord_id, start_date, end_date,
        # rent_amount, rent_due_day, move_in_date.
        # tenant_id is optional, let's remove it to test default handling if any, or just absence.
        del lease_data["tenant_id"]
        del lease_data["security_deposit"]

        now = datetime.utcnow() # For comparison if created_at/updated_at are auto-set

        lease = Lease(
            lease_id=lease_data["lease_id"],
            property_id=lease_data["property_id"],
            landlord_id=lease_data["landlord_id"],
            start_date=lease_data["start_date"],
            end_date=lease_data["end_date"],
            rent_amount=lease_data["rent_amount"],
            rent_due_day=lease_data["rent_due_day"],
            move_in_date=lease_data["move_in_date"]
            # Assuming tenant_id, rent_start_date, security_deposit, notes, signature_requests are optional
            # and will take their default values (often None or empty list).
        )

        self.assertEqual(lease.lease_id, lease_data["lease_id"])
        self.assertEqual(lease.property_id, lease_data["property_id"])
        self.assertEqual(lease.landlord_id, lease_data["landlord_id"])
        self.assertEqual(lease.start_date, lease_data["start_date"])
        self.assertEqual(lease.end_date, lease_data["end_date"])
        self.assertEqual(lease.rent_amount, lease_data["rent_amount"])
        self.assertEqual(lease.rent_due_day, lease_data["rent_due_day"])
        self.assertEqual(lease.move_in_date, lease_data["move_in_date"])

        # Test default values
        self.assertEqual(lease.status, LeaseStatusType.DRAFT)
        self.assertEqual(lease.signing_status, LeaseSigningStatus.NOT_STARTED)

        # Test default rent_start_date logic
        self.assertEqual(lease.rent_start_date, lease.move_in_date)

        # Test other optional fields are defaults (None or empty)
        self.assertIsNone(lease.tenant_id) # Assuming tenant_id is None if not provided
        self.assertIsNone(lease.security_deposit) # Assuming security_deposit is None if not provided
        self.assertIsNone(lease.notes)
        self.assertEqual(lease.signature_requests, []) # Assuming it defaults to an empty list

        # Optionally check timestamps if they are auto-generated and accessible
        # self.assertIsNotNone(lease.created_at)
        # self.assertLessEqual((now - lease.created_at).total_seconds(), 5) # within 5 seconds

    def test_lease_rent_start_date_explicit(self):
        """Test Lease instantiation with an explicit rent_start_date."""
        explicit_rent_start_date = date(2024, 1, 15)
        lease_data = {
            **self.common_lease_data,
            "rent_start_date": explicit_rent_start_date
        }

        lease = Lease(**lease_data)

        self.assertEqual(lease.rent_start_date, explicit_rent_start_date)
        self.assertNotEqual(lease.rent_start_date, lease.move_in_date) # Ensure it's not defaulting

    def test_lease_decimal_field(self):
        """Test that monetary fields are stored as Decimal."""
        rent = Decimal("1500.75")
        deposit = Decimal("2000.50")

        lease_data = self.common_lease_data.copy()
        lease_data["rent_amount"] = rent
        lease_data["security_deposit"] = deposit

        lease = Lease(**lease_data)

        self.assertIsInstance(lease.rent_amount, Decimal)
        self.assertEqual(lease.rent_amount, rent)
        self.assertIsInstance(lease.security_deposit, Decimal)
        self.assertEqual(lease.security_deposit, deposit)

    def test_lease_optional_fields(self):
        """Test Lease instantiation with some optional fields set and others None."""
        custom_notes = "This is a special lease agreement."
        tenant_id_val = 405

        lease_data = self.common_lease_data.copy()
        lease_data["notes"] = custom_notes
        lease_data["tenant_id"] = tenant_id_val
        # Let security_deposit be None (remove it if it's in common_lease_data and we want to test None)
        if "security_deposit" in lease_data:
            del lease_data["security_deposit"]

        lease = Lease(**lease_data)

        self.assertEqual(lease.notes, custom_notes)
        self.assertEqual(lease.tenant_id, tenant_id_val)
        self.assertIsNone(lease.security_deposit) # Assuming it defaults to None if not provided

        # Test default for signature_requests if not provided
        self.assertEqual(lease.signature_requests, [])

        # Test with signature_requests provided
        sig_requests_data = [{"signer_email": "test@example.com", "status": "sent"}]
        lease_data_with_sigs = {**lease_data, "signature_requests": sig_requests_data}
        lease_with_sigs = Lease(**lease_data_with_sigs)
        self.assertEqual(lease_with_sigs.signature_requests, sig_requests_data)


if __name__ == '__main__':
    unittest.main()
