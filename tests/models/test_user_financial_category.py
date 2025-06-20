import unittest
from datetime import datetime
from models.user_financial_category import UserFinancialCategory, FinancialTransactionType

class TestUserFinancialCategory(unittest.TestCase):

    def test_instantiation_landlord_custom_category(self):
        """Test instantiation for a landlord's custom category."""
        now = datetime.utcnow()
        category = UserFinancialCategory(
            category_id=1,
            landlord_id=101,
            name="Late Fee Income",
            type=FinancialTransactionType.INCOME
            # is_system_default defaults to False
        )

        self.assertEqual(category.category_id, 1)
        self.assertEqual(category.landlord_id, 101)
        self.assertEqual(category.name, "Late Fee Income")
        self.assertEqual(category.type, FinancialTransactionType.INCOME)
        self.assertIsInstance(category.type, FinancialTransactionType)

        # Check defaults
        self.assertFalse(category.is_system_default)
        self.assertIsNone(category.description)
        self.assertIsInstance(category.created_at, datetime)
        self.assertIsInstance(category.updated_at, datetime)
        self.assertTrue((category.created_at - now).total_seconds() < 5)
        self.assertTrue((category.updated_at - now).total_seconds() < 5)

    def test_instantiation_system_default_category(self):
        """Test instantiation for a system-default category."""
        now = datetime.utcnow()
        category = UserFinancialCategory(
            category_id=10,
            landlord_id=None, # System categories have no landlord_id
            name="General Repairs",
            type=FinancialTransactionType.EXPENSE,
            is_system_default=True
        )
        self.assertEqual(category.category_id, 10)
        self.assertIsNone(category.landlord_id)
        self.assertEqual(category.name, "General Repairs")
        self.assertEqual(category.type, FinancialTransactionType.EXPENSE)
        self.assertTrue(category.is_system_default)
        self.assertIsInstance(category.created_at, datetime) # Check default timestamp
        self.assertTrue((category.created_at - now).total_seconds() < 5)


    def test_instantiation_with_all_fields(self):
        """Test instantiation with all fields provided."""
        created_ts = datetime(2023,1,1,8,0,0)
        updated_ts = datetime(2023,1,2,9,0,0)

        category = UserFinancialCategory(
            category_id=3,
            landlord_id=102,
            name="Custom Utility Payments",
            type=FinancialTransactionType.EXPENSE,
            is_system_default=False, # Explicitly for a custom one
            description="Specific utility payments for Property X.",
            created_at=created_ts,
            updated_at=updated_ts
        )

        self.assertEqual(category.category_id, 3)
        self.assertEqual(category.landlord_id, 102)
        self.assertEqual(category.name, "Custom Utility Payments")
        self.assertEqual(category.type, FinancialTransactionType.EXPENSE)
        self.assertFalse(category.is_system_default)
        self.assertEqual(category.description, "Specific utility payments for Property X.")
        self.assertEqual(category.created_at, created_ts)
        self.assertEqual(category.updated_at, updated_ts)

    def test_boolean_and_enum_types(self):
        """Test types of boolean and enum fields."""
        cat_income = UserFinancialCategory(4, 103, "Test Income", FinancialTransactionType.INCOME)
        self.assertIsInstance(cat_income.type, FinancialTransactionType)
        self.assertFalse(cat_income.is_system_default) # Default

        cat_expense_system = UserFinancialCategory(
            5, None, "System Expense", FinancialTransactionType.EXPENSE, is_system_default=True
        )
        self.assertIsInstance(cat_expense_system.type, FinancialTransactionType)
        self.assertTrue(cat_expense_system.is_system_default)

    def test_datetime_types(self):
        """Test types of datetime fields."""
        cat = UserFinancialCategory(6, 104, "Time Test", FinancialTransactionType.INCOME)
        self.assertIsInstance(cat.created_at, datetime)
        self.assertIsInstance(cat.updated_at, datetime)

        custom_time = datetime(2022,10,10,10,10,10)
        cat_custom_time = UserFinancialCategory(
            7, 105, "Custom Time Test", FinancialTransactionType.EXPENSE,
            created_at=custom_time, updated_at=custom_time
        )
        self.assertEqual(cat_custom_time.created_at, custom_time)
        self.assertEqual(cat_custom_time.updated_at, custom_time)


if __name__ == '__main__':
    unittest.main()
