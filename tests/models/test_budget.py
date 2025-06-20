import unittest
from datetime import datetime, date
from models.budget import Budget # Removed BudgetItem, BudgetPeriodType as they are not used by Budget model

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

if __name__ == '__main__':
    unittest.main()
