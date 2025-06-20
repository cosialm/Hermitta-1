import unittest
from datetime import datetime, date
from decimal import Decimal
from models.quote import Quote, QuoteStatus

class TestQuote(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test Quote instantiation with only required fields."""
        now = datetime.utcnow()
        quote_amount = Decimal("100.00")

        quote = Quote(
            quote_id=1,
            maintenance_request_id=101,
            vendor_user_id=201,
            landlord_user_id=301,
            amount=quote_amount,
            description_of_work="Fix leaking faucet in kitchen."
        )

        self.assertEqual(quote.quote_id, 1)
        self.assertEqual(quote.maintenance_request_id, 101)
        self.assertEqual(quote.vendor_user_id, 201)
        self.assertEqual(quote.landlord_user_id, 301)
        self.assertEqual(quote.amount, quote_amount)
        self.assertIsInstance(quote.amount, Decimal)
        self.assertEqual(quote.description_of_work, "Fix leaking faucet in kitchen.")

        # Check defaults
        self.assertEqual(quote.status, QuoteStatus.DRAFT)
        self.assertIsInstance(quote.status, QuoteStatus)
        self.assertIsInstance(quote.created_at, datetime)
        self.assertIsInstance(quote.updated_at, datetime)
        self.assertTrue((quote.created_at - now).total_seconds() < 5)
        self.assertTrue((quote.updated_at - now).total_seconds() < 5)

        # Check other optionals are None
        self.assertIsNone(quote.valid_until)
        self.assertIsNone(quote.submitted_at)
        self.assertIsNone(quote.approved_or_rejected_at)
        self.assertIsNone(quote.landlord_comments)
        self.assertIsNone(quote.vendor_comments)
        self.assertIsNone(quote.quote_document_id)

    def test_instantiation_with_all_fields(self):
        """Test Quote instantiation with all fields provided."""
        valid_date = date(2024, 12, 31)
        submitted_ts = datetime(2024, 1, 1, 10, 0, 0)
        approved_ts = datetime(2024, 1, 2, 11, 0, 0)
        created_ts = datetime(2024,1,1,9,0,0)
        updated_ts = datetime(2024,1,2,11,5,0)
        quote_amount = Decimal("250.50")

        quote = Quote(
            quote_id=2,
            maintenance_request_id=102,
            vendor_user_id=202,
            landlord_user_id=302,
            amount=quote_amount,
            description_of_work="Replace broken window pane, living room.",
            valid_until=valid_date,
            status=QuoteStatus.APPROVED,
            submitted_at=submitted_ts,
            approved_or_rejected_at=approved_ts,
            landlord_comments="Approved, proceed with repair.",
            vendor_comments="Includes cost of glass and labor.",
            quote_document_id=501, # FK to Document model
            created_at=created_ts,
            updated_at=updated_ts
        )

        self.assertEqual(quote.quote_id, 2)
        self.assertEqual(quote.maintenance_request_id, 102)
        # ... (check all other fields)
        self.assertEqual(quote.valid_until, valid_date)
        self.assertIsInstance(quote.valid_until, date)
        self.assertEqual(quote.status, QuoteStatus.APPROVED)
        self.assertEqual(quote.submitted_at, submitted_ts)
        self.assertIsInstance(quote.submitted_at, datetime)
        self.assertEqual(quote.approved_or_rejected_at, approved_ts)
        self.assertIsInstance(quote.approved_or_rejected_at, datetime)
        self.assertEqual(quote.landlord_comments, "Approved, proceed with repair.")
        self.assertEqual(quote.vendor_comments, "Includes cost of glass and labor.")
        self.assertEqual(quote.quote_document_id, 501)
        self.assertEqual(quote.created_at, created_ts)
        self.assertEqual(quote.updated_at, updated_ts)

    def test_default_status_is_draft(self):
        """Test that the default status is DRAFT."""
        quote = Quote(
            quote_id=3, maintenance_request_id=103, vendor_user_id=203, landlord_user_id=303,
            amount=Decimal("50.00"), description_of_work="Inspect AC unit."
        )
        self.assertEqual(quote.status, QuoteStatus.DRAFT)

    def test_decimal_date_datetime_enum_types(self):
        """Test types of Decimal, date, datetime, and enum fields."""
        quote = Quote(
            quote_id=4, maintenance_request_id=104, vendor_user_id=204, landlord_user_id=304,
            amount=Decimal("75.20"), description_of_work="Pest control service.",
            valid_until=date(2025, 1, 1),
            status=QuoteStatus.SUBMITTED,
            submitted_at=datetime.utcnow()
        )
        self.assertIsInstance(quote.amount, Decimal)
        self.assertIsInstance(quote.valid_until, date)
        self.assertIsInstance(quote.status, QuoteStatus)
        self.assertIsInstance(quote.submitted_at, datetime)
        self.assertIsInstance(quote.created_at, datetime)
        self.assertIsInstance(quote.updated_at, datetime)
        self.assertIsNone(quote.approved_or_rejected_at) # Check None for optional datetime

if __name__ == '__main__':
    unittest.main()
