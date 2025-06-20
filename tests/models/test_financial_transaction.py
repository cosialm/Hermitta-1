import unittest
from datetime import datetime, date
from decimal import Decimal
from models.financial_transaction import (
    FinancialTransaction, FinancialTransactionType, RecurrenceFrequency
)

class TestFinancialTransaction(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test FinancialTransaction instantiation with only required fields."""
        now = datetime.utcnow()
        tx_date = date(2024, 1, 15)
        amount_decimal = Decimal("100.50")

        tx = FinancialTransaction(
            transaction_id=1,
            landlord_id=101,
            type=FinancialTransactionType.INCOME,
            category_id=1, # e.g., "Rent Income"
            description="January Rent for Unit A1",
            amount=amount_decimal,
            transaction_date=tx_date
        )

        self.assertEqual(tx.transaction_id, 1)
        self.assertEqual(tx.landlord_id, 101)
        self.assertEqual(tx.type, FinancialTransactionType.INCOME)
        self.assertIsInstance(tx.type, FinancialTransactionType)
        self.assertEqual(tx.category_id, 1)
        self.assertEqual(tx.description, "January Rent for Unit A1")
        self.assertEqual(tx.amount, amount_decimal)
        self.assertIsInstance(tx.amount, Decimal)
        self.assertEqual(tx.transaction_date, tx_date)
        self.assertIsInstance(tx.transaction_date, date)

        # Check defaults
        self.assertFalse(tx.is_recurring)
        self.assertFalse(tx.is_tax_deductible_candidate)
        self.assertIsInstance(tx.created_at, datetime)
        self.assertIsInstance(tx.updated_at, datetime)
        self.assertTrue((tx.created_at - now).total_seconds() < 5)
        self.assertTrue((tx.updated_at - now).total_seconds() < 5)

        # Check other optionals are None
        self.assertIsNone(tx.property_id)
        self.assertIsNone(tx.lease_id)
        self.assertIsNone(tx.related_payment_id)
        self.assertIsNone(tx.maintenance_request_id)
        self.assertIsNone(tx.document_id)
        self.assertIsNone(tx.vendor_name)
        self.assertIsNone(tx.sub_category)
        self.assertIsNone(tx.recurrence_frequency)
        self.assertIsNone(tx.recurrence_end_date)
        self.assertIsNone(tx.next_due_date)
        self.assertIsNone(tx.parent_recurring_transaction_id)
        self.assertIsNone(tx.notes)

    def test_instantiation_with_all_fields(self):
        """Test FinancialTransaction instantiation with all fields provided."""
        tx_date = date(2024, 2, 20)
        rec_end_date = date(2025, 2, 20)
        next_due = date(2024, 3, 20)
        created = datetime(2024,2,20,10,0,0)
        updated = datetime(2024,2,20,11,0,0)

        tx = FinancialTransaction(
            transaction_id=2, landlord_id=102, type=FinancialTransactionType.EXPENSE,
            category_id=2, description="Monthly Internet Bill", amount=Decimal("50.00"),
            transaction_date=tx_date, property_id=201, lease_id=301, related_payment_id=401,
            maintenance_request_id=501, document_id=601, vendor_name="ISP Corp",
            sub_category="Internet", is_recurring=True,
            recurrence_frequency=RecurrenceFrequency.MONTHLY,
            recurrence_end_date=rec_end_date, next_due_date=next_due,
            parent_recurring_transaction_id=None, # Master recurring record
            is_tax_deductible_candidate=True, notes="Regular utility payment.",
            created_at=created, updated_at=updated
        )

        self.assertEqual(tx.transaction_id, 2)
        self.assertEqual(tx.landlord_id, 102)
        self.assertEqual(tx.type, FinancialTransactionType.EXPENSE)
        self.assertEqual(tx.category_id, 2)
        self.assertEqual(tx.description, "Monthly Internet Bill")
        self.assertEqual(tx.amount, Decimal("50.00"))
        self.assertEqual(tx.transaction_date, tx_date)
        self.assertEqual(tx.property_id, 201)
        self.assertEqual(tx.lease_id, 301)
        self.assertEqual(tx.related_payment_id, 401)
        self.assertEqual(tx.maintenance_request_id, 501)
        self.assertEqual(tx.document_id, 601)
        self.assertEqual(tx.vendor_name, "ISP Corp")
        self.assertEqual(tx.sub_category, "Internet")
        self.assertTrue(tx.is_recurring)
        self.assertEqual(tx.recurrence_frequency, RecurrenceFrequency.MONTHLY)
        self.assertIsInstance(tx.recurrence_frequency, RecurrenceFrequency)
        self.assertEqual(tx.recurrence_end_date, rec_end_date)
        self.assertIsInstance(tx.recurrence_end_date, date)
        self.assertEqual(tx.next_due_date, next_due)
        self.assertIsInstance(tx.next_due_date, date)
        self.assertIsNone(tx.parent_recurring_transaction_id)
        self.assertTrue(tx.is_tax_deductible_candidate)
        self.assertEqual(tx.notes, "Regular utility payment.")
        self.assertEqual(tx.created_at, created)
        self.assertEqual(tx.updated_at, updated)

    def test_recurring_transaction_instance(self):
        """Test instantiation of an instance of a recurring transaction."""
        tx_date = date(2024, 3, 10)
        tx_instance = FinancialTransaction(
            transaction_id=3, landlord_id=102, type=FinancialTransactionType.EXPENSE,
            category_id=2, description="Monthly Internet Bill - March", amount=Decimal("50.00"),
            transaction_date=tx_date, property_id=201,
            parent_recurring_transaction_id=2 # Links to the master record (tx_id=2)
        )
        self.assertEqual(tx_instance.parent_recurring_transaction_id, 2)
        self.assertFalse(tx_instance.is_recurring) # Instance itself is not a master recurring tx

    def test_decimal_and_date_types(self):
        """Test Decimal and date/datetime types."""
        tx = FinancialTransaction(
            transaction_id=4, landlord_id=101, type=FinancialTransactionType.INCOME,
            category_id=1, description="Test", amount=Decimal("0.01"),
            transaction_date=date.today(),
            recurrence_end_date=date.today(), # Also test optional date field
            next_due_date=date.today()        # Also test optional date field
        )
        self.assertIsInstance(tx.amount, Decimal)
        self.assertIsInstance(tx.transaction_date, date)
        self.assertIsInstance(tx.created_at, datetime)
        self.assertIsInstance(tx.updated_at, datetime)
        self.assertIsInstance(tx.recurrence_end_date, date)
        self.assertIsInstance(tx.next_due_date, date)

    def test_boolean_flags_defaults_and_set(self):
        """Test boolean flags default to False and can be set."""
        tx_default = FinancialTransaction(
            transaction_id=5, landlord_id=101, type=FinancialTransactionType.INCOME,
            category_id=1, description="Test Default Flags", amount=Decimal("10.00"),
            transaction_date=date.today()
        )
        self.assertFalse(tx_default.is_recurring)
        self.assertFalse(tx_default.is_tax_deductible_candidate)

        tx_set = FinancialTransaction(
            transaction_id=6, landlord_id=101, type=FinancialTransactionType.EXPENSE,
            category_id=2, description="Test Set Flags", amount=Decimal("20.00"),
            transaction_date=date.today(),
            is_recurring=True,
            is_tax_deductible_candidate=True
        )
        self.assertTrue(tx_set.is_recurring)
        self.assertTrue(tx_set.is_tax_deductible_candidate)

if __name__ == '__main__':
    unittest.main()
