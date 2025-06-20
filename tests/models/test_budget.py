import unittest
from datetime import datetime, date
from decimal import Decimal
from models.budget import Budget, BudgetItem # Added BudgetItem, BudgetPeriodType if needed later

class TestBudget(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test Budget instantiation with only required fields."""
        start_date = date(2024, 1, 1)
        end_date = date(2024, 12, 31)
        now = datetime.utcnow() # For created_at/updated_at comparison

        budget = Budget(
            budget_id=1,
            landlord_id=101,
            name="Annual General Budget 2024",
            period_start_date=start_date,
            period_end_date=end_date
        )

        self.assertEqual(budget.budget_id, 1)
        self.assertEqual(budget.landlord_id, 101)
        self.assertEqual(budget.name, "Annual General Budget 2024")
        self.assertEqual(budget.period_start_date, start_date)
        self.assertIsInstance(budget.period_start_date, date)
        self.assertEqual(budget.period_end_date, end_date)
        self.assertIsInstance(budget.period_end_date, date)

        self.assertIsNone(budget.property_id)
        self.assertIsNone(budget.notes)

        self.assertIsInstance(budget.created_at, datetime)
        self.assertIsInstance(budget.updated_at, datetime)
        # Check if timestamps are close to 'now' (within a few seconds)
        self.assertTrue((budget.created_at - now).total_seconds() < 5)
        self.assertTrue((budget.updated_at - now).total_seconds() < 5)
        # Check that updated_at is same or newer than created_at by default
        self.assertTrue(budget.updated_at >= budget.created_at)


    def test_instantiation_with_all_fields(self):
        """Test Budget instantiation with all fields, including optional ones."""
        start_date = date(2024, 3, 1)
        end_date = date(2024, 5, 31)
        created_ts = datetime(2024, 2, 1, 10, 0, 0)
        updated_ts = datetime(2024, 2, 15, 11, 30, 0)

        budget = Budget(
            budget_id=2,
            landlord_id=102,
            name="Q2 Property Maintenance Budget",
            period_start_date=start_date,
            period_end_date=end_date,
            property_id=201,
            notes="Focus on plumbing and electrical for Property Alpha.",
            created_at=created_ts,
            updated_at=updated_ts
        )

        self.assertEqual(budget.budget_id, 2)
        self.assertEqual(budget.landlord_id, 102)
        self.assertEqual(budget.name, "Q2 Property Maintenance Budget")
        self.assertEqual(budget.period_start_date, start_date)
        self.assertEqual(budget.period_end_date, end_date)
        self.assertEqual(budget.property_id, 201)
        self.assertEqual(budget.notes, "Focus on plumbing and electrical for Property Alpha.")
        self.assertEqual(budget.created_at, created_ts)
        self.assertEqual(budget.updated_at, updated_ts)

    def test_date_and_datetime_field_types(self):
        """Test the types of date and datetime fields."""
        start_date = date(2023, 1, 1)
        end_date = date(2023, 1, 31)
        custom_created_at = datetime(2023,1,1,0,0,0)
        custom_updated_at = datetime(2023,1,1,1,0,0)

        # Test with default datetime fields
        budget1 = Budget(
            budget_id=3, landlord_id=103, name="Default Time Budget",
            period_start_date=start_date, period_end_date=end_date
        )
        self.assertIsInstance(budget1.period_start_date, date)
        self.assertIsInstance(budget1.period_end_date, date)
        self.assertIsInstance(budget1.created_at, datetime)
        self.assertIsInstance(budget1.updated_at, datetime)

        # Test with specified datetime fields
        budget2 = Budget(
            budget_id=4, landlord_id=104, name="Specific Time Budget",
            period_start_date=start_date, period_end_date=end_date,
            created_at=custom_created_at, updated_at=custom_updated_at
        )
        self.assertIsInstance(budget2.period_start_date, date)
        self.assertIsInstance(budget2.period_end_date, date)
        self.assertEqual(budget2.created_at, custom_created_at)
        self.assertIsInstance(budget2.created_at, datetime)
        self.assertEqual(budget2.updated_at, custom_updated_at)
        self.assertIsInstance(budget2.updated_at, datetime)

    def test_default_timestamps_logic(self):
        """Test that default timestamps are set correctly and updated_at >= created_at."""
        budget = Budget(
            budget_id=5,
            landlord_id=105,
            name="Timestamp Test Budget",
            period_start_date=date(2025,1,1),
            period_end_date=date(2025,1,31)
        )
        # Allow a small delta for creation time
        delta_seconds = 2
        now = datetime.utcnow()

        time_diff_created = (now - budget.created_at).total_seconds()
        self.assertTrue(abs(time_diff_created) < delta_seconds, f"created_at timestamp {budget.created_at} is too far from current time {now}")

        time_diff_updated = (now - budget.updated_at).total_seconds()
        self.assertTrue(abs(time_diff_updated) < delta_seconds, f"updated_at timestamp {budget.updated_at} is too far from current time {now}")

        self.assertTrue(budget.updated_at >= budget.created_at)


class TestBudgetItem(unittest.TestCase):

    def test_budget_item_instantiation_required(self):
        """Test BudgetItem instantiation with only required fields."""
        budgeted_amount_val = Decimal("1500.75")
        item = BudgetItem(
            budget_item_id=1,
            budget_id=10,
            category_id=5,
            budgeted_amount=budgeted_amount_val
        )

        self.assertEqual(item.budget_item_id, 1)
        self.assertEqual(item.budget_id, 10)
        self.assertEqual(item.category_id, 5)
        self.assertEqual(item.budgeted_amount, budgeted_amount_val)
        self.assertIsInstance(item.budgeted_amount, Decimal)
        self.assertIsNone(item.notes)

    def test_budget_item_instantiation_all_fields(self):
        """Test BudgetItem instantiation with all fields, including notes."""
        budgeted_amount_val = Decimal("200.00")
        notes_val = "Monthly internet service fee"
        item = BudgetItem(
            budget_item_id=2,
            budget_id=11,
            category_id=6,
            budgeted_amount=budgeted_amount_val,
            notes=notes_val
        )

        self.assertEqual(item.budget_item_id, 2)
        self.assertEqual(item.budget_id, 11)
        self.assertEqual(item.category_id, 6)
        self.assertEqual(item.budgeted_amount, budgeted_amount_val)
        self.assertIsInstance(item.budgeted_amount, Decimal)
        self.assertEqual(item.notes, notes_val)

    def test_budget_item_decimal_amount(self):
        """Test that budgeted_amount is correctly stored as Decimal."""
        # Test with a whole number
        amount_whole = Decimal("500")
        item1 = BudgetItem(budget_item_id=3, budget_id=12, category_id=7, budgeted_amount=amount_whole)
        self.assertEqual(item1.budgeted_amount, amount_whole)
        self.assertIsInstance(item1.budgeted_amount, Decimal)

        # Test with decimal places
        amount_decimal = Decimal("123.45")
        item2 = BudgetItem(budget_item_id=4, budget_id=13, category_id=8, budgeted_amount=amount_decimal)
        self.assertEqual(item2.budgeted_amount, amount_decimal)
        self.assertIsInstance(item2.budgeted_amount, Decimal)

        # Test with initialization from string
        amount_from_string = Decimal("99.99")
        item3 = BudgetItem(budget_item_id=5, budget_id=14, category_id=9, budgeted_amount=amount_from_string)
        self.assertEqual(item3.budgeted_amount, Decimal("99.99")) # Ensure it's the same Decimal value
        self.assertIsInstance(item3.budgeted_amount, Decimal)


if __name__ == '__main__':
    unittest.main()
