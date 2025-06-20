import unittest
from datetime import datetime
from models.maintenance_request_vendor_assignment import (
    MaintenanceRequestVendorAssignment, VendorAssignmentStatus
)

class TestMaintenanceRequestVendorAssignment(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test instantiation with only required fields and default values."""
        now = datetime.utcnow()
        assignment = MaintenanceRequestVendorAssignment(
            assignment_id=1,
            request_id=101, # FK to MaintenanceRequest
            vendor_id=201    # FK to User (Vendor)
        )

        self.assertEqual(assignment.assignment_id, 1)
        self.assertEqual(assignment.request_id, 101)
        self.assertEqual(assignment.vendor_id, 201)

        # Check defaults
        self.assertIsInstance(assignment.assigned_at, datetime)
        self.assertTrue((assignment.assigned_at - now).total_seconds() < 5)
        self.assertEqual(assignment.status, VendorAssignmentStatus.PENDING_ACCEPTANCE)
        self.assertIsInstance(assignment.status, VendorAssignmentStatus)

        # Check other optionals are None
        self.assertIsNone(assignment.vendor_quote_id)
        self.assertIsNone(assignment.vendor_specific_instructions)
        self.assertIsNone(assignment.accepted_at)
        self.assertIsNone(assignment.declined_at)
        self.assertIsNone(assignment.work_started_at)
        self.assertIsNone(assignment.work_completed_at)
        self.assertIsNone(assignment.cancelled_at)

    def test_instantiation_with_all_fields(self):
        """Test instantiation with all fields provided."""
        assigned_ts = datetime(2023,1,1,10,0,0)
        accepted_ts = datetime(2023,1,1,12,0,0)
        declined_ts = None # Mutually exclusive with accepted_ts usually
        work_started_ts = datetime(2023,1,2,9,0,0)
        work_completed_ts = datetime(2023,1,2,17,0,0)
        cancelled_ts = None # Mutually exclusive

        assignment = MaintenanceRequestVendorAssignment(
            assignment_id=2,
            request_id=102,
            vendor_id=202,
            assigned_at=assigned_ts,
            status=VendorAssignmentStatus.ACCEPTED,
            vendor_quote_id=301, # FK to Quote
            vendor_specific_instructions="Please use the back entrance.",
            accepted_at=accepted_ts,
            declined_at=declined_ts,
            work_started_at=work_started_ts,
            work_completed_at=work_completed_ts,
            cancelled_at=cancelled_ts
        )

        self.assertEqual(assignment.assignment_id, 2)
        self.assertEqual(assignment.request_id, 102)
        self.assertEqual(assignment.vendor_id, 202)
        self.assertEqual(assignment.assigned_at, assigned_ts)
        self.assertEqual(assignment.status, VendorAssignmentStatus.ACCEPTED)
        self.assertEqual(assignment.vendor_quote_id, 301)
        self.assertEqual(assignment.vendor_specific_instructions, "Please use the back entrance.")
        self.assertEqual(assignment.accepted_at, accepted_ts)
        self.assertIsNone(assignment.declined_at) # As it was set to None
        self.assertEqual(assignment.work_started_at, work_started_ts)
        self.assertEqual(assignment.work_completed_at, work_completed_ts)
        self.assertIsNone(assignment.cancelled_at) # As it was set to None

        # Check types of optional datetime fields that were set
        self.assertIsInstance(assignment.accepted_at, datetime)
        self.assertIsInstance(assignment.work_started_at, datetime)
        self.assertIsInstance(assignment.work_completed_at, datetime)


    def test_default_status_is_pending_acceptance(self):
        """Test that the default status is PENDING_ACCEPTANCE."""
        assignment = MaintenanceRequestVendorAssignment(
            assignment_id=3, request_id=103, vendor_id=203
        )
        self.assertEqual(assignment.status, VendorAssignmentStatus.PENDING_ACCEPTANCE)

    def test_datetime_field_types(self):
        """Test types of datetime fields, including when None."""
        assignment_default_times = MaintenanceRequestVendorAssignment(4, 104, 204)
        self.assertIsInstance(assignment_default_times.assigned_at, datetime)
        self.assertIsNone(assignment_default_times.accepted_at)
        self.assertIsNone(assignment_default_times.declined_at)
        # ... and so on for other optional datetimes

        custom_time = datetime(2023, 5, 5, 5, 5, 5)
        assignment_custom_times = MaintenanceRequestVendorAssignment(
            assignment_id=5, request_id=105, vendor_id=205,
            assigned_at=custom_time,
            accepted_at=custom_time,
            declined_at=custom_time, # Though logically one or other would be None
            work_started_at=custom_time,
            work_completed_at=custom_time,
            cancelled_at=custom_time
        )
        self.assertIsInstance(assignment_custom_times.assigned_at, datetime)
        self.assertIsInstance(assignment_custom_times.accepted_at, datetime)
        self.assertIsInstance(assignment_custom_times.declined_at, datetime)
        self.assertIsInstance(assignment_custom_times.work_started_at, datetime)
        self.assertIsInstance(assignment_custom_times.work_completed_at, datetime)
        self.assertIsInstance(assignment_custom_times.cancelled_at, datetime)

if __name__ == '__main__':
    unittest.main()
