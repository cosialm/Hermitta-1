import unittest
from datetime import datetime, date
from decimal import Decimal
from models.maintenance_request import (
    MaintenanceRequest, MaintenanceRequestStatus, MaintenanceRequestCategory, MaintenancePriority
)

class TestMaintenanceRequest(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test MaintenanceRequest instantiation with only required fields."""
        now = datetime.utcnow() # For submitted_at, updated_at comparison
        req = MaintenanceRequest(
            request_id=1,
            property_id=101,
            created_by_user_id=201, # e.g., Tenant User ID
            description="Leaking tap in kitchen.",
            category=MaintenanceRequestCategory.PLUMBING
        )

        self.assertEqual(req.request_id, 1)
        self.assertEqual(req.property_id, 101)
        self.assertEqual(req.created_by_user_id, 201)
        self.assertEqual(req.description, "Leaking tap in kitchen.")
        self.assertEqual(req.category, MaintenanceRequestCategory.PLUMBING)
        self.assertIsInstance(req.category, MaintenanceRequestCategory)

        # Check defaults
        self.assertEqual(req.priority, MaintenancePriority.MEDIUM)
        self.assertIsInstance(req.priority, MaintenancePriority)
        self.assertEqual(req.status, MaintenanceRequestStatus.SUBMITTED_BY_TENANT)
        self.assertIsInstance(req.status, MaintenanceRequestStatus)
        self.assertEqual(req.initial_photo_urls, [])
        self.assertIsInstance(req.initial_photo_urls, list)
        self.assertIsInstance(req.submitted_at, datetime)
        self.assertTrue((req.submitted_at - now).total_seconds() < 5)
        self.assertIsInstance(req.updated_at, datetime)
        self.assertTrue((req.updated_at - now).total_seconds() < 5)

        # Check many other optionals are None
        self.assertIsNone(req.tenant_id)
        self.assertIsNone(req.tenant_contact_preference)
        self.assertIsNone(req.assigned_to_user_id)
        self.assertIsNone(req.assigned_vendor_name_manual)
        self.assertIsNone(req.vendor_assigned_at)
        self.assertIsNone(req.scheduled_date)
        self.assertIsNone(req.resolution_notes)
        self.assertIsNone(req.actual_cost)
        self.assertIsNone(req.tenant_feedback_rating)
        self.assertIsNone(req.tenant_feedback_comment)
        self.assertIsNone(req.resolved_by_user_id)
        self.assertIsNone(req.quote_id)
        self.assertIsNone(req.vendor_invoice_id)
        self.assertIsNone(req.acknowledged_at)
        self.assertIsNone(req.vendor_accepted_at)
        self.assertIsNone(req.quote_approved_at)
        self.assertIsNone(req.work_started_at)
        self.assertIsNone(req.work_completed_at)
        self.assertIsNone(req.tenant_confirmed_at)
        self.assertIsNone(req.invoice_submitted_at)
        self.assertIsNone(req.closed_at)


    def test_instantiation_with_comprehensive_fields(self):
        """Test MaintenanceRequest instantiation with a comprehensive set of fields."""
        s_at = datetime(2023,1,1,10,0,0)
        u_at = datetime(2023,1,15,10,0,0)
        ack_at = datetime(2023,1,1,12,0,0)
        vend_assign_at = datetime(2023,1,2,10,0,0)
        vend_acc_at = datetime(2023,1,2,14,0,0)
        q_appr_at = datetime(2023,1,3,10,0,0)
        w_start_at = datetime(2023,1,4,9,0,0)
        w_comp_at = datetime(2023,1,5,16,0,0)
        t_conf_at = datetime(2023,1,6,10,0,0)
        inv_sub_at = datetime(2023,1,7,11,0,0)
        cl_at = datetime(2023,1,8,12,0,0)
        sched_date = date(2023,1,4)
        photos = ["url1.jpg", "url2.png"]

        req = MaintenanceRequest(
            request_id=2, property_id=102, tenant_id=202, created_by_user_id=202,
            description="Broken window in living room.", category=MaintenanceRequestCategory.STRUCTURAL_ISSUE,
            priority=MaintenancePriority.HIGH, status=MaintenanceRequestStatus.WORK_IN_PROGRESS,
            tenant_contact_preference="Call before arriving", initial_photo_urls=photos,
            assigned_to_user_id=301, # Vendor user ID
            assigned_vendor_name_manual="Backup Glass Co.", # If assigned_to_user_id not used
            scheduled_date=sched_date,
            resolution_notes="Window replaced successfully.", actual_cost=Decimal("150.75"),
            tenant_feedback_rating=5, tenant_feedback_comment="Great job!",
            resolved_by_user_id=301, quote_id=501, vendor_invoice_id=601,
            submitted_at=s_at, acknowledged_at=ack_at, vendor_assigned_at=vend_assign_at,
            vendor_accepted_at=vend_acc_at, quote_approved_at=q_appr_at, work_started_at=w_start_at,
            work_completed_at=w_comp_at, tenant_confirmed_at=t_conf_at,
            invoice_submitted_at=inv_sub_at, closed_at=cl_at, updated_at=u_at
        )

        self.assertEqual(req.request_id, 2)
        self.assertEqual(req.property_id, 102)
        self.assertEqual(req.tenant_id, 202)
        self.assertEqual(req.created_by_user_id, 202)
        self.assertEqual(req.description, "Broken window in living room.")
        self.assertEqual(req.category, MaintenanceRequestCategory.STRUCTURAL_ISSUE)
        self.assertEqual(req.priority, MaintenancePriority.HIGH)
        self.assertEqual(req.status, MaintenanceRequestStatus.WORK_IN_PROGRESS)
        self.assertEqual(req.tenant_contact_preference, "Call before arriving")
        self.assertEqual(req.initial_photo_urls, photos)
        self.assertEqual(req.assigned_to_user_id, 301)
        self.assertEqual(req.assigned_vendor_name_manual, "Backup Glass Co.")
        self.assertEqual(req.scheduled_date, sched_date)
        self.assertIsInstance(req.scheduled_date, date)
        self.assertEqual(req.resolution_notes, "Window replaced successfully.")
        self.assertEqual(req.actual_cost, Decimal("150.75"))
        self.assertIsInstance(req.actual_cost, Decimal)
        self.assertEqual(req.tenant_feedback_rating, 5)
        self.assertEqual(req.tenant_feedback_comment, "Great job!")
        self.assertEqual(req.resolved_by_user_id, 301)
        self.assertEqual(req.quote_id, 501)
        self.assertEqual(req.vendor_invoice_id, 601)
        self.assertEqual(req.submitted_at, s_at)
        self.assertEqual(req.acknowledged_at, ack_at)
        self.assertEqual(req.vendor_assigned_at, vend_assign_at) # Check both vendor_assigned_at assignments
        self.assertEqual(req.vendor_accepted_at, vend_acc_at)
        self.assertEqual(req.quote_approved_at, q_appr_at)
        self.assertEqual(req.work_started_at, w_start_at)
        self.assertEqual(req.work_completed_at, w_comp_at)
        self.assertEqual(req.tenant_confirmed_at, t_conf_at)
        self.assertEqual(req.invoice_submitted_at, inv_sub_at)
        self.assertEqual(req.closed_at, cl_at)
        self.assertEqual(req.updated_at, u_at)

        # Check types of all datetime optional fields
        for dt_field_val in [req.acknowledged_at, req.vendor_assigned_at, req.vendor_accepted_at,
                             req.quote_approved_at, req.work_started_at, req.work_completed_at,
                             req.tenant_confirmed_at, req.invoice_submitted_at, req.closed_at]:
            self.assertIsInstance(dt_field_val, datetime)


    def test_initial_photo_urls_defaults_to_empty_list(self):
        """Test that initial_photo_urls defaults to an empty list."""
        req_no_photos = MaintenanceRequest(
            request_id=3, property_id=103, created_by_user_id=203,
            description="Test", category=MaintenanceRequestCategory.OTHER
        )
        self.assertEqual(req_no_photos.initial_photo_urls, [])
        self.assertIsInstance(req_no_photos.initial_photo_urls, list)

        req_photos_none = MaintenanceRequest(
            request_id=4, property_id=104, created_by_user_id=204,
            description="Test", category=MaintenanceRequestCategory.OTHER, initial_photo_urls=None
        )
        self.assertEqual(req_photos_none.initial_photo_urls, [])

    def test_default_enum_values(self):
        """Test default values for Priority and Status enums."""
        req = MaintenanceRequest(
            request_id=5, property_id=105, created_by_user_id=205,
            description="Test defaults", category=MaintenanceRequestCategory.ELECTRICAL
        )
        self.assertEqual(req.priority, MaintenancePriority.MEDIUM)
        self.assertEqual(req.status, MaintenanceRequestStatus.SUBMITTED_BY_TENANT)

if __name__ == '__main__':
    unittest.main()
