import unittest
from datetime import datetime
from models.application_screening import ApplicationScreening, ScreeningType, ScreeningStatus

class TestApplicationScreening(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test instantiation with only required fields and default values."""
        now = datetime.utcnow() # For updated_at comparison
        screening = ApplicationScreening(
            screening_id=1,
            application_id=101,
            screening_type=ScreeningType.CREDIT_CHECK
        )
        self.assertEqual(screening.screening_id, 1)
        self.assertEqual(screening.application_id, 101)
        self.assertEqual(screening.screening_type, ScreeningType.CREDIT_CHECK)
        self.assertEqual(screening.status, ScreeningStatus.PENDING_REQUEST) # Default
        self.assertIsNone(screening.reference_contact_name)
        self.assertIsNone(screening.reference_contact_details)
        self.assertIsNone(screening.screening_notes)
        self.assertIsNone(screening.provider_name)
        self.assertIsNone(screening.provider_reference_id)
        self.assertIsNone(screening.report_summary)
        self.assertIsNone(screening.screening_report_document_id)
        self.assertIsNone(screening.requested_at)
        self.assertIsNone(screening.completed_at)
        self.assertIsInstance(screening.updated_at, datetime)
        # Check if updated_at is close to 'now' (within a few seconds)
        self.assertTrue((screening.updated_at - now).total_seconds() < 5)

    def test_instantiation_with_all_fields(self):
        """Test instantiation with all fields provided."""
        custom_time_updated = datetime(2023, 1, 1, 12, 0, 0)
        custom_time_requested = datetime(2023, 1, 1, 10, 0, 0)
        custom_time_completed = datetime(2023, 1, 1, 11, 0, 0)

        screening = ApplicationScreening(
            screening_id=2,
            application_id=102,
            screening_type=ScreeningType.MANUAL_REFERENCE_CHECK,
            status=ScreeningStatus.COMPLETED_SUCCESS,
            reference_contact_name="John Doe",
            reference_contact_details="john.doe@example.com",
            screening_notes="Very positive reference.",
            provider_name="Manual Check Inc.", # Can be used for manual too
            provider_reference_id="REF12345",
            report_summary="Tenant confirmed good standing.",
            screening_report_document_id=501,
            requested_at=custom_time_requested,
            completed_at=custom_time_completed,
            updated_at=custom_time_updated
        )
        self.assertEqual(screening.screening_id, 2)
        self.assertEqual(screening.application_id, 102)
        self.assertEqual(screening.screening_type, ScreeningType.MANUAL_REFERENCE_CHECK)
        self.assertEqual(screening.status, ScreeningStatus.COMPLETED_SUCCESS)
        self.assertEqual(screening.reference_contact_name, "John Doe")
        self.assertEqual(screening.reference_contact_details, "john.doe@example.com")
        self.assertEqual(screening.screening_notes, "Very positive reference.")
        self.assertEqual(screening.provider_name, "Manual Check Inc.")
        self.assertEqual(screening.provider_reference_id, "REF12345")
        self.assertEqual(screening.report_summary, "Tenant confirmed good standing.")
        self.assertEqual(screening.screening_report_document_id, 501)
        self.assertEqual(screening.requested_at, custom_time_requested)
        self.assertEqual(screening.completed_at, custom_time_completed)
        self.assertEqual(screening.updated_at, custom_time_updated)

    def test_enum_field_types(self):
        """Test that screening_type and status are instances of their Enums."""
        screening = ApplicationScreening(
            screening_id=3,
            application_id=103,
            screening_type=ScreeningType.BACKGROUND_CHECK,
            status=ScreeningStatus.IN_PROGRESS
        )
        self.assertIsInstance(screening.screening_type, ScreeningType)
        self.assertEqual(screening.screening_type, ScreeningType.BACKGROUND_CHECK)
        self.assertIsInstance(screening.status, ScreeningStatus)
        self.assertEqual(screening.status, ScreeningStatus.IN_PROGRESS)

    def test_datetime_field_types(self):
        """Test that datetime fields are instances of datetime."""
        now = datetime.utcnow()
        screening1 = ApplicationScreening( # Test default updated_at
            screening_id=4, application_id=104,
            screening_type=ScreeningType.CREDIT_CHECK
        )
        self.assertIsInstance(screening1.updated_at, datetime)

        custom_req_time = datetime(2023, 2, 1, 0, 0, 0)
        custom_comp_time = datetime(2023, 2, 2, 0, 0, 0)
        custom_upd_time = datetime(2023, 2, 3, 0, 0, 0)
        screening2 = ApplicationScreening(
            screening_id=5, application_id=105,
            screening_type=ScreeningType.MANUAL_EMPLOYER_CHECK,
            requested_at=custom_req_time,
            completed_at=custom_comp_time,
            updated_at=custom_upd_time
        )
        self.assertIsInstance(screening2.requested_at, datetime)
        self.assertEqual(screening2.requested_at, custom_req_time)
        self.assertIsInstance(screening2.completed_at, datetime)
        self.assertEqual(screening2.completed_at, custom_comp_time)
        self.assertIsInstance(screening2.updated_at, datetime)
        self.assertEqual(screening2.updated_at, custom_upd_time)

    def test_status_default_value(self):
        """Test that status defaults to PENDING_REQUEST."""
        screening = ApplicationScreening(
            screening_id=6,
            application_id=106,
            screening_type=ScreeningType.CREDIT_CHECK
        )
        self.assertEqual(screening.status, ScreeningStatus.PENDING_REQUEST)

    def test_optional_fields_default_to_none(self):
        """Test that optional fields default to None if not provided."""
        screening = ApplicationScreening(
            screening_id=7,
            application_id=107,
            screening_type=ScreeningType.BACKGROUND_CHECK
        )
        self.assertIsNone(screening.reference_contact_name)
        self.assertIsNone(screening.reference_contact_details)
        self.assertIsNone(screening.screening_notes)
        self.assertIsNone(screening.provider_name)
        self.assertIsNone(screening.provider_reference_id)
        self.assertIsNone(screening.report_summary)
        self.assertIsNone(screening.screening_report_document_id)
        self.assertIsNone(screening.requested_at)
        self.assertIsNone(screening.completed_at)

if __name__ == '__main__':
    unittest.main()
