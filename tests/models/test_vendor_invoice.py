import unittest
from datetime import datetime, date, timedelta
from decimal import Decimal
from models.vendor_invoice import VendorInvoice, VendorInvoiceStatus

class TestVendorInvoice(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test VendorInvoice instantiation with only required fields."""
        now = datetime.utcnow()
        due_dt = date.today() + timedelta(days=30)
        amount = Decimal("500.00")

        invoice = VendorInvoice(
            invoice_id=1,
            maintenance_request_id=101,
            vendor_user_id=201,
            landlord_user_id=301,
            invoice_number="INV-001",
            amount_due=amount,
            due_date=due_dt
            # status defaults to SUBMITTED, submitted_at should auto-set
        )

        self.assertEqual(invoice.invoice_id, 1)
        self.assertEqual(invoice.maintenance_request_id, 101)
        self.assertEqual(invoice.vendor_user_id, 201)
        self.assertEqual(invoice.landlord_user_id, 301)
        self.assertEqual(invoice.invoice_number, "INV-001")
        self.assertEqual(invoice.amount_due, amount)
        self.assertIsInstance(invoice.amount_due, Decimal)
        self.assertEqual(invoice.due_date, due_dt)
        self.assertIsInstance(invoice.due_date, date)

        # Check defaults
        self.assertEqual(invoice.status, VendorInvoiceStatus.SUBMITTED)
        self.assertIsInstance(invoice.status, VendorInvoiceStatus)
        self.assertIsInstance(invoice.submitted_at, datetime) # Auto-set for SUBMITTED status
        self.assertTrue((invoice.submitted_at - now).total_seconds() < 5)
        self.assertIsInstance(invoice.created_at, datetime)
        self.assertIsInstance(invoice.updated_at, datetime)
        self.assertTrue((invoice.created_at - now).total_seconds() < 5) # created_at also defaults to now

        # Check other optionals are None
        self.assertIsNone(invoice.quote_id)
        self.assertIsNone(invoice.payment_instructions)
        self.assertIsNone(invoice.approved_at)
        self.assertIsNone(invoice.paid_at)
        self.assertIsNone(invoice.invoice_document_id)
        self.assertIsNone(invoice.linked_financial_transaction_id)
        self.assertIsNone(invoice.notes_by_vendor)
        self.assertIsNone(invoice.notes_by_landlord)

    def test_submitted_at_logic_on_instantiation(self):
        """Test submitted_at logic based on status during instantiation."""
        now = datetime.utcnow()
        due_dt = date.today() + timedelta(days=30)
        amount = Decimal("100.00")

        # Case 1: Status SUBMITTED, submitted_at is None (should auto-set)
        inv_submitted_auto = VendorInvoice(
            1, 1, 1, 1, "INV01", amount, due_dt, status=VendorInvoiceStatus.SUBMITTED
        )
        self.assertIsInstance(inv_submitted_auto.submitted_at, datetime)
        self.assertTrue((inv_submitted_auto.submitted_at - now).total_seconds() < 5)

        # Case 2: Status SUBMITTED, submitted_at is provided
        custom_submit_time = now - timedelta(hours=2)
        inv_submitted_custom = VendorInvoice(
            2, 1, 1, 1, "INV02", amount, due_dt,
            status=VendorInvoiceStatus.SUBMITTED, submitted_at=custom_submit_time
        )
        self.assertEqual(inv_submitted_custom.submitted_at, custom_submit_time)

        # Case 3: Status DRAFT, submitted_at is None (should be None)
        inv_draft_none = VendorInvoice(
            3, 1, 1, 1, "INV03", amount, due_dt, status=VendorInvoiceStatus.DRAFT
        )
        self.assertIsNone(inv_draft_none.submitted_at)

        # Case 4: Status DRAFT, submitted_at is provided (should be respected)
        inv_draft_custom = VendorInvoice(
            4, 1, 1, 1, "INV04", amount, due_dt,
            status=VendorInvoiceStatus.DRAFT, submitted_at=custom_submit_time
        )
        self.assertEqual(inv_draft_custom.submitted_at, custom_submit_time)


    def test_instantiation_with_all_fields(self):
        """Test VendorInvoice instantiation with all fields provided."""
        due_dt = date(2024, 5, 31)
        c_at = datetime(2024,4,1,10,0,0)
        u_at = datetime(2024,4,15,10,0,0)
        s_at = datetime(2024,4,1,11,0,0)
        appr_at = datetime(2024,4,2,12,0,0)
        p_at = datetime(2024,4,10,14,0,0)

        invoice = VendorInvoice(
            invoice_id=5, maintenance_request_id=105, vendor_user_id=205, landlord_user_id=305,
            invoice_number="INV-2024-005", amount_due=Decimal("1250.75"), due_date=due_dt,
            quote_id=50, status=VendorInvoiceStatus.PAID,
            payment_instructions="Pay via M-Pesa Paybill 123456, Acc: INV-2024-005",
            submitted_at=s_at, approved_at=appr_at, paid_at=p_at,
            invoice_document_id=705, linked_financial_transaction_id=805,
            notes_by_vendor="Materials and labor included.",
            notes_by_landlord="Payment confirmed via bank transfer.",
            created_at=c_at, updated_at=u_at
        )
        self.assertEqual(invoice.invoice_id, 5)
        # ... (check all other fields)
        self.assertEqual(invoice.quote_id, 50)
        self.assertEqual(invoice.status, VendorInvoiceStatus.PAID)
        self.assertEqual(invoice.payment_instructions, "Pay via M-Pesa Paybill 123456, Acc: INV-2024-005")
        self.assertEqual(invoice.submitted_at, s_at)
        self.assertEqual(invoice.approved_at, appr_at)
        self.assertIsInstance(invoice.approved_at, datetime)
        self.assertEqual(invoice.paid_at, p_at)
        self.assertIsInstance(invoice.paid_at, datetime)
        self.assertEqual(invoice.invoice_document_id, 705)
        self.assertEqual(invoice.linked_financial_transaction_id, 805)
        self.assertEqual(invoice.notes_by_vendor, "Materials and labor included.")
        self.assertEqual(invoice.notes_by_landlord, "Payment confirmed via bank transfer.")
        self.assertEqual(invoice.created_at, c_at)
        self.assertEqual(invoice.updated_at, u_at)

    def test_default_status_is_submitted(self):
        """Test that the default status is SUBMITTED."""
        invoice = VendorInvoice(6,1,1,1,"INV06",Decimal("1.00"),date.today())
        self.assertEqual(invoice.status, VendorInvoiceStatus.SUBMITTED)

    def test_types_of_fields(self):
        """Test various field types like Decimal, date, datetime, Enum."""
        invoice = VendorInvoice(
            7,1,1,1,"INV07",Decimal("99.99"),date(2025,1,15),
            status=VendorInvoiceStatus.APPROVED_FOR_PAYMENT,
            approved_at=datetime.utcnow()
        )
        self.assertIsInstance(invoice.amount_due, Decimal)
        self.assertIsInstance(invoice.due_date, date)
        self.assertIsInstance(invoice.status, VendorInvoiceStatus)
        self.assertIsInstance(invoice.approved_at, datetime)
        self.assertIsInstance(invoice.created_at, datetime)
        self.assertIsInstance(invoice.updated_at, datetime)
        self.assertIsNone(invoice.paid_at) # Optional datetime

if __name__ == '__main__':
    unittest.main()
