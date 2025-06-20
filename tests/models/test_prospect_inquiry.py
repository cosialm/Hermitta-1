import unittest
from datetime import datetime
from models.prospect_inquiry import ProspectInquiry, ProspectInquiryStatus

class TestProspectInquiry(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test ProspectInquiry instantiation with only required fields."""
        now = datetime.utcnow()
        inquiry = ProspectInquiry(
            inquiry_id=1,
            property_id=101,
            landlord_id=201,
            prospect_name="John Doe",
            prospect_email="john.doe@example.com"
        )

        self.assertEqual(inquiry.inquiry_id, 1)
        self.assertEqual(inquiry.property_id, 101)
        self.assertEqual(inquiry.landlord_id, 201)
        self.assertEqual(inquiry.prospect_name, "John Doe")
        self.assertEqual(inquiry.prospect_email, "john.doe@example.com")

        # Check defaults
        self.assertIsInstance(inquiry.received_at, datetime)
        self.assertTrue((inquiry.received_at - now).total_seconds() < 5)
        self.assertIsInstance(inquiry.updated_at, datetime)
        self.assertTrue((inquiry.updated_at - now).total_seconds() < 5)
        self.assertEqual(inquiry.status, ProspectInquiryStatus.NEW)
        self.assertIsInstance(inquiry.status, ProspectInquiryStatus)

        # Check other optionals are None
        self.assertIsNone(inquiry.prospect_phone)
        self.assertIsNone(inquiry.message)
        self.assertIsNone(inquiry.preferred_contact_method)
        self.assertIsNone(inquiry.source)
        self.assertIsNone(inquiry.internal_notes)

    def test_instantiation_with_all_fields(self):
        """Test ProspectInquiry instantiation with all fields provided."""
        received_ts = datetime(2023,1,1,10,0,0)
        updated_ts = datetime(2023,1,1,11,0,0)

        inquiry = ProspectInquiry(
            inquiry_id=2,
            property_id=102,
            landlord_id=202,
            prospect_name="Jane Smith",
            prospect_email="jane.smith@example.com",
            prospect_phone="254712345679",
            message="Interested in the 3-bedroom unit. Availability and viewing times?",
            preferred_contact_method="EMAIL",
            source="Company Website",
            received_at=received_ts,
            status=ProspectInquiryStatus.CONTACTED,
            internal_notes="Emailed prospect with viewing slots.",
            updated_at=updated_ts
        )

        self.assertEqual(inquiry.inquiry_id, 2)
        self.assertEqual(inquiry.property_id, 102)
        self.assertEqual(inquiry.landlord_id, 202)
        self.assertEqual(inquiry.prospect_name, "Jane Smith")
        self.assertEqual(inquiry.prospect_email, "jane.smith@example.com")
        self.assertEqual(inquiry.prospect_phone, "254712345679")
        self.assertEqual(inquiry.message, "Interested in the 3-bedroom unit. Availability and viewing times?")
        self.assertEqual(inquiry.preferred_contact_method, "EMAIL")
        self.assertEqual(inquiry.source, "Company Website")
        self.assertEqual(inquiry.received_at, received_ts)
        self.assertEqual(inquiry.status, ProspectInquiryStatus.CONTACTED)
        self.assertEqual(inquiry.internal_notes, "Emailed prospect with viewing slots.")
        self.assertEqual(inquiry.updated_at, updated_ts)

    def test_default_status_is_new(self):
        """Test that the default status is NEW."""
        inquiry = ProspectInquiry(
            inquiry_id=3, property_id=103, landlord_id=203,
            prospect_name="Test User", prospect_email="test@example.com"
        )
        self.assertEqual(inquiry.status, ProspectInquiryStatus.NEW)
        self.assertIsInstance(inquiry.status, ProspectInquiryStatus)

    def test_datetime_and_enum_types(self):
        """Test types of datetime and enum fields."""
        inquiry = ProspectInquiry(
            inquiry_id=4, property_id=104, landlord_id=204,
            prospect_name="Type Test", prospect_email="type@example.com",
            status=ProspectInquiryStatus.VIEWING_SCHEDULED,
            received_at=datetime(2022,12,25,8,0,0)
        )
        self.assertIsInstance(inquiry.received_at, datetime)
        self.assertIsInstance(inquiry.updated_at, datetime) # Should still default
        self.assertIsInstance(inquiry.status, ProspectInquiryStatus)

if __name__ == '__main__':
    unittest.main()
