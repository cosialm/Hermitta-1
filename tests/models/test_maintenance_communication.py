import unittest
from datetime import datetime
from models.maintenance_communication import MaintenanceCommunication

class TestMaintenanceCommunication(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test MaintenanceCommunication instantiation with only required fields."""
        now = datetime.utcnow()
        comm = MaintenanceCommunication(
            comm_id=1,
            maintenance_request_id=101,
            user_id=201, # Tenant, Landlord, Staff, or Vendor
            message_text="The issue is still ongoing."
        )

        self.assertEqual(comm.comm_id, 1)
        self.assertEqual(comm.maintenance_request_id, 101)
        self.assertEqual(comm.user_id, 201)
        self.assertEqual(comm.message_text, "The issue is still ongoing.")

        # Check defaults
        self.assertIsInstance(comm.sent_at, datetime)
        self.assertTrue((comm.sent_at - now).total_seconds() < 5)
        self.assertFalse(comm.is_internal_note) # Default False

    def test_instantiation_with_all_fields(self):
        """Test MaintenanceCommunication instantiation with all fields, including optionals."""
        custom_sent_at = datetime(2023, 1, 1, 12, 30, 0)
        comm = MaintenanceCommunication(
            comm_id=2,
            maintenance_request_id=102,
            user_id=301, # e.g., Landlord
            message_text="This is an internal note regarding the repair.",
            sent_at=custom_sent_at,
            is_internal_note=True
        )

        self.assertEqual(comm.comm_id, 2)
        self.assertEqual(comm.maintenance_request_id, 102)
        self.assertEqual(comm.user_id, 301)
        self.assertEqual(comm.message_text, "This is an internal note regarding the repair.")
        self.assertEqual(comm.sent_at, custom_sent_at)
        self.assertIsInstance(comm.sent_at, datetime)
        self.assertTrue(comm.is_internal_note)

    def test_is_internal_note_flag(self):
        """Test the is_internal_note boolean flag."""
        # Default is False (checked in required_fields test)

        # Explicitly False
        comm_public = MaintenanceCommunication(
            comm_id=3, maintenance_request_id=103, user_id=202,
            message_text="Public message.", is_internal_note=False
        )
        self.assertFalse(comm_public.is_internal_note)

        # Explicitly True
        comm_internal = MaintenanceCommunication(
            comm_id=4, maintenance_request_id=104, user_id=302,
            message_text="Internal note.", is_internal_note=True
        )
        self.assertTrue(comm_internal.is_internal_note)

    def test_datetime_field_type(self):
        """Test the type of the datetime field."""
        comm_default_time = MaintenanceCommunication(
            comm_id=5, maintenance_request_id=105, user_id=205, message_text="Time test"
        )
        self.assertIsInstance(comm_default_time.sent_at, datetime)

        custom_time = datetime(2022, 11, 10, 10, 0, 0)
        comm_custom_time = MaintenanceCommunication(
            comm_id=6, maintenance_request_id=106, user_id=206, message_text="Custom time test",
            sent_at=custom_time
        )
        self.assertIsInstance(comm_custom_time.sent_at, datetime)
        self.assertEqual(comm_custom_time.sent_at, custom_time)

if __name__ == '__main__':
    unittest.main()
