import unittest
from datetime import datetime, timedelta
from decimal import Decimal
from models.rental_application import (
    RentalApplication, RentalApplicationStatus, ApplicationFeeStatus
)

class TestRentalApplication(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test RentalApplication instantiation with only required fields."""
        now = datetime.utcnow()
        app = RentalApplication(
            application_id=1,
            property_id=101,
            full_name="John Applicant",
            email="john.applicant@example.com",
            phone_number="0712345678"
        )

        self.assertEqual(app.application_id, 1)
        self.assertEqual(app.property_id, 101)
        self.assertEqual(app.full_name, "John Applicant")
        self.assertEqual(app.email, "john.applicant@example.com")
        self.assertEqual(app.phone_number, "0712345678")

        # Check defaults
        self.assertIsNone(app.applicant_user_id)
        self.assertEqual(app.application_data, {})
        self.assertIsInstance(app.application_data, dict)
        self.assertEqual(app.custom_fields_data, {})
        self.assertIsInstance(app.custom_fields_data, dict)
        self.assertEqual(app.status, RentalApplicationStatus.DRAFT)
        self.assertIsInstance(app.status, RentalApplicationStatus)
        self.assertIsNone(app.submitted_at) # Status is DRAFT
        self.assertIsNone(app.reviewed_at)
        self.assertIsNone(app.notes_for_landlord)
        self.assertIsNone(app.internal_notes)
        self.assertFalse(app.applicant_consent_data_processing)
        self.assertFalse(app.applicant_consent_background_check)
        self.assertIsNone(app.application_fee_amount)
        self.assertEqual(app.application_fee_paid_status, ApplicationFeeStatus.NOT_APPLICABLE)
        self.assertIsInstance(app.application_fee_paid_status, ApplicationFeeStatus)
        self.assertIsInstance(app.created_at, datetime)
        self.assertIsInstance(app.updated_at, datetime)
        self.assertTrue((app.created_at - now).total_seconds() < 5)
        self.assertTrue((app.updated_at - now).total_seconds() < 5)


    def test_submitted_at_logic_on_instantiation(self):
        """Test submitted_at logic based on status during instantiation."""
        now = datetime.utcnow()

        # Case 1: Status SUBMITTED, submitted_at is None (should auto-set)
        app_submitted_auto_time = RentalApplication(
            application_id=2, property_id=102, full_name="Jane Submitter",
            email="jane.s@example.com", phone_number="0722000111",
            status=RentalApplicationStatus.SUBMITTED
        )
        self.assertIsInstance(app_submitted_auto_time.submitted_at, datetime)
        self.assertTrue((app_submitted_auto_time.submitted_at - now).total_seconds() < 5)

        # Case 2: Status SUBMITTED, submitted_at is provided
        custom_submit_time = now - timedelta(hours=1)
        app_submitted_custom_time = RentalApplication(
            application_id=3, property_id=103, full_name="Peter Submitter",
            email="peter.s@example.com", phone_number="0733000222",
            status=RentalApplicationStatus.SUBMITTED,
            submitted_at=custom_submit_time
        )
        self.assertEqual(app_submitted_custom_time.submitted_at, custom_submit_time)

        # Case 3: Status DRAFT, submitted_at is provided (should respect it, though unusual)
        app_draft_custom_time = RentalApplication(
            application_id=4, property_id=104, full_name="Drafty McDraftFace",
            email="drafty@example.com", phone_number="0744000333",
            status=RentalApplicationStatus.DRAFT,
            submitted_at=custom_submit_time
        )
        self.assertEqual(app_draft_custom_time.submitted_at, custom_submit_time)

        # Case 4: Status DRAFT, submitted_at is None (should be None)
        app_draft_no_time = RentalApplication(
            application_id=5, property_id=105, full_name="Still Drafting",
            email="still.drafting@example.com", phone_number="0755000444",
            status=RentalApplicationStatus.DRAFT
        )
        self.assertIsNone(app_draft_no_time.submitted_at)


    def test_instantiation_with_all_fields(self):
        """Test RentalApplication instantiation with all fields provided."""
        app_data = {"income": "50000"}
        custom_data = {"pets": "1 cat"}
        fee = Decimal("50.00")
        c_at = datetime(2023,1,1,8,0,0)
        u_at = datetime(2023,1,1,9,0,0)
        s_at = datetime(2023,1,1,8,30,0) # submitted before updated
        r_at = datetime(2023,1,1,10,0,0)

        app = RentalApplication(
            application_id=6, property_id=106, full_name="All Fields Applicant",
            email="all@example.com", phone_number="0766000555",
            applicant_user_id=206,
            application_data=app_data, custom_fields_data=custom_data,
            status=RentalApplicationStatus.APPROVED, submitted_at=s_at, reviewed_at=r_at,
            notes_for_landlord="Looking forward to hearing from you.",
            internal_notes="Seems like a good candidate.",
            applicant_consent_data_processing=True,
            applicant_consent_background_check=True,
            application_fee_amount=fee,
            application_fee_paid_status=ApplicationFeeStatus.PAID,
            created_at=c_at, updated_at=u_at
        )
        self.assertEqual(app.application_id, 6)
        self.assertEqual(app.property_id, 106)
        self.assertEqual(app.applicant_user_id, 206)
        self.assertEqual(app.application_data, app_data)
        self.assertEqual(app.custom_fields_data, custom_data)
        self.assertEqual(app.status, RentalApplicationStatus.APPROVED)
        self.assertEqual(app.submitted_at, s_at)
        self.assertEqual(app.reviewed_at, r_at)
        self.assertEqual(app.notes_for_landlord, "Looking forward to hearing from you.")
        self.assertEqual(app.internal_notes, "Seems like a good candidate.")
        self.assertTrue(app.applicant_consent_data_processing)
        self.assertTrue(app.applicant_consent_background_check)
        self.assertEqual(app.application_fee_amount, fee)
        self.assertIsInstance(app.application_fee_amount, Decimal)
        self.assertEqual(app.application_fee_paid_status, ApplicationFeeStatus.PAID)
        self.assertIsInstance(app.application_fee_paid_status, ApplicationFeeStatus)
        self.assertEqual(app.created_at, c_at)
        self.assertEqual(app.updated_at, u_at)

    def test_data_dictionaries_default_to_empty_dict(self):
        """Test that data dictionaries default to empty dicts."""
        app1 = RentalApplication(1,1,"N1","e1@c.c","p1", application_data=None)
        self.assertEqual(app1.application_data, {})

        app2 = RentalApplication(2,1,"N2","e2@c.c","p2", custom_fields_data=None)
        self.assertEqual(app2.custom_fields_data, {})

        app3 = RentalApplication(3,1,"N3","e3@c.c","p3") # Omitted
        self.assertEqual(app3.application_data, {})
        self.assertEqual(app3.custom_fields_data, {})

    def test_enum_and_boolean_types(self):
        """Test enum and boolean field types and defaults."""
        app = RentalApplication(4,1,"N4","e4@c.c","p4")
        self.assertIsInstance(app.status, RentalApplicationStatus)
        self.assertIsInstance(app.application_fee_paid_status, ApplicationFeeStatus)
        self.assertFalse(app.applicant_consent_data_processing) # Default
        self.assertFalse(app.applicant_consent_background_check) # Default

        app_consents_true = RentalApplication(
            5,1,"N5","e5@c.c","p5",
            applicant_consent_data_processing=True,
            applicant_consent_background_check=True
        )
        self.assertTrue(app_consents_true.applicant_consent_data_processing)
        self.assertTrue(app_consents_true.applicant_consent_background_check)

if __name__ == '__main__':
    unittest.main()
